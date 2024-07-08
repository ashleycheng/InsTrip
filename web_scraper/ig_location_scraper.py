import requests

from loguru import logger
from time import sleep as wait
from sqlalchemy import text

from router import Router


def header() -> dict:
    return {
        "Accept": "*/*",
        "Accept-Language": "zh-TW,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Referer": "https://www.instagram.com/explore/locations/287620626/busan-south-korea/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "X-Csrftoken": "P3IkLxjuDX1nOmnuC108zegywl1i1Hcf",
        "X-Ig-App-Id": "936619743392459",
    }

def get_location_info(location_id: str) -> dict:
    url = f'https://www.instagram.com/api/v1/locations/web_info/?location_id={location_id}&show_nearby=false&skip_recent_tab=false'
    post = requests.get(url, headers=header())
    context = post.json()
    try:
        info = context['native_location_data']['location_info']

        return {
                'location_id': location_id,
                'name': info['name'],
                'category': info['category'],
                'lat': info['lat'],
                'lng': info['lng'],
                'location_address': info['location_address'],
                'location_city': info['location_city'],
               }
    except:
        return {}

def main():
    db_router = Router()
    mycursor = db_router.mysql_traveldata_conn
    sql = """SELECT distinct location_id, location_city, counrty from IgPost WHERE location_id is not null"""
    data_tmp = mycursor.execute(text(sql))
    res = data_tmp.fetchall()

    for i in res:
        sql = f"""SELECT count(*) from IgLocation WHERE location_id = {i[0]}"""
        data_tmp = mycursor.execute(text(sql))
        if data_tmp.fetchall()[0][0] > 0:
            continue
        try:
            loc = get_location_info(i[0])
            logger.info(loc)
        
            mycursor = db_router.mysql_traveldata_conn
            sql = "INSERT INTO IgLocation (location_id, location_name, location_city, country, category, address, city, lat, lng) VALUES (:location_id, :location_name, :location_city, :country, :category, :address, :city, :lat, :lng)"
            val = {
                "location_id": loc['location_id'], "location_name": loc['name'], "location_city": i[1], 
                "country": i[2], "category": loc['category'], "address": loc['location_address'], "city": loc['location_city'], 
                "lat": str(loc['lat']), "lng": str(loc['lng'])}
            mycursor.execute(text(sql), val)
            mycursor.commit()
            wait(30)

        except Exception as e:
            logger.error(e)

    logger.info("Sccuess: the task is done.")


if __name__ == "__main__":
    main()
