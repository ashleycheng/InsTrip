# InsTrip
This project built a travel website called [InsTrip](https://ashleycheng.pythonanywhere.com/) , which makes users to explore the most popular cities and photo spots on Instagram. It also provides AI-generated(ChatGPT) attraction recommendations for the cities with the most tourists.  


## System architecture
<img width="1074" alt="image" src="https://github.com/ashleycheng/InsTrip/assets/17893844/977c8c33-87cf-4957-8de5-6aac161be3ba">


## Data model
<img width="1020" alt="image" src="https://github.com/ashleycheng/InsTrip/assets/17893844/162742e4-685c-4263-8c8d-e877b772df63">

## Get started
### 1. Build MySQL database using Docker
Create the Dockerfile `mysql.yml`:
```
version: '3.3'
services:

  mysql:
      image: mysql:8.0
      command: mysqld --default-authentication-plugin=mysql_native_password
      ports:
          - 3307:3306
      environment:
          MYSQL_DATABASE: YOUR_DB_NAME
          MYSQL_USER: YOUR_DB_USER_NAME
          MYSQL_PASSWORD: YOUR_DB_PASSWORD
          MYSQL_ROOT_PASSWORD: YOUR_DB_PASSWORD
      volumes:
          - mysql:/var/lib/mysql
      networks:
          - dev

  phpmyadmin:
      image: phpmyadmin/phpmyadmin:5.1.0
      links:
          - mysql:db
      ports:
          - 8000:80
      depends_on:
        - mysql
      networks:
          - dev

networks:
  dev:

volumes:
  mysql:
    external: true
```

Run `mysql.yml` to create the docker container for DB and phpmyadmin tool in the background:
```
docker-compose -f mysql.yml up -d
```

### 2. Set up environment
Build the virtual environment and install python and node packages:
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ npm install
```


Set environment variables needed in this project:
```
$ export DB_USER=YOUR_DB_USER_NAME \
  export DB_PASSWORD=YOUR_DB_PASSWORD \
  export DB_HOST=YOUR_DB_HOST \
  export DB_PORT=YOUR_DB_PORT \
  export DB_NAME=YOUR_DB_NAME \
  export API_TOKEN=YOUR_API_TOKEN \
  export IG_ACCOUNT=YOUR_IG_ACCOUNT \
  export IG_PASSWORD=YOUR_IG_PASSWORD
```

## Run the web scraper to get public data on Instagram
Here are two web scrapers that can be executed through any scheduling tool.
- [ig_post_scraper.py](https://github.com/ashleycheng/InsTrip/blob/main/web_scraper/ig_post_scraper.py): extract posts with travel hastag, like: `#日本旅遊` or `#韓國旅遊`.
- [ig_location_scraper.py](https://github.com/ashleycheng/InsTrip/blob/main/web_scraper/ig_location_scraper.py): extract location information of the posts with check-in.
```
$ python web_scraper/ig_post_scraper.py [country name]
$ python web_scraper/ig_location_scraper.py
```

## API document
### Endpoint
- `api/top/city/{country}`: get the ranking of the most popular cities among tourists on Instagram
- `api/city/{city}/info`: get the city information
- `api/top/location/{city}`: get the ranking of the most popular photo attractions (group by the category of attractions)

<img width="1162" alt="image" src="https://github.com/ashleycheng/InsTrip/assets/17893844/9c44a99d-1436-48e0-ad98-275b99a1b18a">
<img width="1165" alt="image" src="https://github.com/ashleycheng/InsTrip/assets/17893844/26256e01-78cf-4ab2-917d-57becd2c8e7b">
<img width="1162" alt="image" src="https://github.com/ashleycheng/InsTrip/assets/17893844/429bbef2-b8e5-4c29-a109-f9e5e551e657">

