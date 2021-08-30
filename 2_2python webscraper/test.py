import json
from bs4 import BeautifulSoup
from lxml import html
import requests
import cloudscraper

main_url = "https://public.api.nicovideo.jp/v2/wakutkool/frames.json?names=pc-mypage-formation&names=pc-mypage-overlay-banner&tags=userpage&responseType=pc";

r = requests.get(main_url);
print(r.text);

# scraper = cloudscraper.create_scraper();
# web_text = scraper.get(main_url).text;

# print(web_text);