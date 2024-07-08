import json
import os
import random
import re
import requests
import sys

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from latest_user_agents import get_random_user_agent
from loguru import logger
from time import sleep as wait
from sqlalchemy import text

from router import Router


def header(csrf="9YuxzGOfF9_Tqluj-hr6to") -> dict:
    user_agent = get_random_user_agent()
    return {
        "Accept": "*/*",
        "Accept-Language": "zh-TW,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Referer": "https://www.instagram.com/explore/tags/foods/?__a=1",
        'User-Agent': user_agent,
        "X-Requested-With": "XMLHttpRequest",
        "X-Csrftoken": csrf,
        "X-Ig-App-Id": "936619743392459",
    }


def get_location_of_post(
    shortcode: str, 
    session, 
    csrf=None
    ) -> dict:
    """
    Get the check-in information of the post. (this API might be blocked when requested very frequently.)
    """
    url = f'https://www.instagram.com/graphql/query/?variables={{"shortcode": "{shortcode}" }}&query_hash=b3055c01b4b222b8a47dc12b090e4e64'
    post = session.get(url, headers=header(csrf))
    context = post.json()
    try:
        return {"status": "success", "location": context['data']['shortcode_media']['location']}
    except:
        if post.status_code == 401:
            return {"status": "fail", "location": None}
        return {"status": "success", "location": None}


def main(country: str):
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.now().timestamp())

    ig_account = os.getenv("IG_ACCOUNT")
    ig_password = os.getenv("IG_PASSWORD")

    payload = {
        'username': ig_account,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{ig_password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    with requests.Session() as s:
        user_agent = get_random_user_agent()
        r = s.get(link)
        csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
        r = s.post(login_url, data=payload, headers={
            'User-Agent': user_agent,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        })

        next_page = True
        ori_url = f"https://www.instagram.com/api/v1/tags/logged_out_web_info/?tag_name={country}旅遊"
        url = ori_url

        # set the begin time of data
        data_begin_time = (datetime.strptime(
            '2024-01-01', "%Y-%m-%d")).timestamp()
        false_cnt = 0
        db_router = Router()
        counrty = country
        while next_page:
            res = requests.get(url, headers=header()).json()
            for i in res['data']['hashtag']['edge_hashtag_to_media']['edges']:
                """
                record the false count to stop the function when all of the new data already been extracted in DB
                """
                if false_cnt > 10:
                    next_page = False
                    logger.info('stop the scraper function.')
                    break

                if i['node']['taken_at_timestamp'] < data_begin_time:
                    """
                    check the timestamp of data, make sure the data is no earlier than the begin time.
                    """
                    false_cnt += 1
                    logger.warning('The data is earlier than begin time: ' +
                                   datetime.fromtimestamp(i['node']['taken_at_timestamp']))
                    continue
                else:
                    false_cnt = 0

                logger.info('shortcode: ' + i['node']['shortcode'])
                logger.info(
                    'timestamp: ' + str(datetime.fromtimestamp(i['node']['taken_at_timestamp'])))

                try:
                    shortcode = i['node']['shortcode']
                    owner_id = i['node']['owner']['id']
                    content = i['node']['edge_media_to_caption']['edges'][0]['node']['text']
                    date = datetime.fromtimestamp(
                        i['node']['taken_at_timestamp']).date()
                except:
                    logger.warning('content error')
                    continue

                """
                check whether the data is already in DB
                """
                db_router = Router()
                mycursor = db_router.mysql_traveldata_conn
                sql = f"""SELECT count(*) from IgPost WHERE shortcode = '{shortcode}'"""
                data_tmp = mycursor.execute(text(sql))
                if data_tmp.fetchall()[0][0] > 0:
                    logger.info('The record is existed.')
                    false_cnt += 1
                    continue

                wait(random.randint(5, 30))

                """
                check whether the post with check-in and location information.
                """
                location = get_location_of_post(shortcode, s, csrf)
                if location['status'] == "fail":
                    logger.error('The scraper is blocked.')
                    wait(650)
                    false_cnt += 1
                    continue
                    # next_page = False
                    # break
                elif location['location']:
                    logger.info('location info: '+ location['location']['id'] + 
                                location['location']['name'])
                    location_id = location['location']['id']
                    location_name = location['location']['name']
                    address = json.loads(location['location']['address_json'])
                    if address:
                        location_city = address['city_name']
                    else:
                        pass

                    try:
                        """
                        Insert the data to DB.
                        """
                        mycursor = db_router.mysql_traveldata_conn
                        sql = "INSERT INTO IgPost (shortcode, owner_id, content, date, location_id, location_name, location_city, counrty, has_location) VALUES (:shortcode, :owner_id, :content, :date, :location_id, :location_name, :location_city, :counrty, :has_location)"
                        val = {"shortcode": shortcode, "owner_id": owner_id, "content": content, "date": date, "location_id": location_id,
                               "location_name": location_name, "location_city": location_city, "counrty": counrty, "has_location": 1}
                        mycursor.execute(text(sql), val)
                        mycursor.commit()
                    except Exception as e:
                        logger.error(e)
                else:
                    logger.info("There is no location for this post.")
                    try:
                        mycursor = db_router.mysql_traveldata_conn
                        sql = "INSERT INTO IgPost (shortcode, owner_id, content, date, counrty, has_location) VALUES (:shortcode, :owner_id, :content, :date, :counrty, :has_location)"
                        val = {"shortcode": shortcode, "owner_id": owner_id, "content": content, "date": date,
                               "counrty": counrty, "has_location": 0}
                        mycursor.execute(text(sql), val)
                        mycursor.commit()
                    except Exception as e:
                        logger.error(e)

            end_cursor = res['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            url = ori_url + f"&&max_id={end_cursor}"
            logger.info('next url: ' + url)


if __name__ == "__main__":
    country = sys.argv[1]
    main(country)
