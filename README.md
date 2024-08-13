# InsTrip
This project built a travel website called [InsTrip](https://ashleycheng.pythonanywhere.com/) , which makes users to explore the most popular travel cities and photo spots on Instagram. To analyze Instagram data, this project created web scrapers to extract Instagram posts with travel-related hashtags and check-in data. It also used ChatGPT to provide travel destination introductions based on data analysis charts.


## Tech stack
<img width="700" alt="image" src="https://github.com/user-attachments/assets/6092af82-5e88-4ffd-89cc-eb453ff468ad">



## Data model
<img width="1020" alt="image" src="https://github.com/ashleycheng/InsTrip/assets/17893844/162742e4-685c-4263-8c8d-e877b772df63">

## Get started
### 1. Set up environment
Create `.env` file to set environment variables needed in this project.
```
DB_USER=YOUR_DB_USER_NAME 
DB_PASSWORD=YOUR_DB_PASSWORD 
DB_HOST=YOUR_DB_HOST
DB_PORT=YOUR_DB_PORT 
DB_NAME=YOUR_DB_NAME 
API_TOKEN=YOUR_API_TOKEN 
IG_ACCOUNT=YOUR_IG_ACCOUNT 
IG_PASSWORD=YOUR_IG_PASSWORD
```
### 2. Launch the web app using Docker

Run `docker-compose.yml` to create the docker container for the Django web application.
```
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

## Run the web scrapers to get public data on Instagram
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

