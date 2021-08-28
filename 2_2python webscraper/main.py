from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import os
"""
    sample urls
    https://www.xinmeitulu.com/mote/ninjaazhaizhai
    https://www.xinmeitulu.com/mote/baiyin81
    https://www.xinmeitulu.com/mote/coserxiaocangqiandaiw
    https://www.xinmeitulu.com/mote/chunmomo
    https://tw.xinmeitulu.com/mote/cosermizhimaoqiu
    https://tw.xinmeitulu.com/mote/coseryanjiangdamowangw

"""

main_url = "https://tw.xinmeitulu.com/mote/coseryanjiangdamowangw";
# enter the url you want, make sure the ending does not have page number

directory = "D:/trying"; # modify this to change directory


def count_pages(page_set):
    page_count = 1;
    if not page_set == None:
        pages = page_set.find_all("li");
        
        page_count = int(pages[len(pages)-2].text);
            
    return page_count;

def single_page_scrape(driver):
    html = driver.page_source;
    soup = BeautifulSoup(html,"html.parser");
    all_figures = soup.find_all("figure", class_ = "figure");
    all_url = [];
    for figure_url in all_figures:
        all_url.append(figure_url.a["href"]);
        # print(href_link);
    driver.close();
    for href_link in all_url:
        scrape_page_and_save(get_page_driver(href_link));

def get_page_driver(url):
    driver = webdriver.Chrome("./chromedriver");
    driver.get(url);
    time.sleep(5);
    
    return driver;

def multi_page_scrape(page_count):
    for page_number in range(page_count):
        
        page_driver = get_page_driver(f"{main_url}/page/{page_number+1}");

        single_page_scrape(page_driver);

def scrape_page_and_save(driver):
    html = driver.page_source;
    soup = BeautifulSoup(html,"html.parser");

    all_divs = soup.find_all("img", class_ = "figure-img img-fluid rounded");

    title_content = soup.find("h1", class_ = "h3");

    folder_name = title_content.text.strip();

    save_directory = f"{directory}/{folder_name}";

    print(save_directory);

    if not os.path.exists(save_directory):
        os.makedirs(save_directory);
    i = 1;
    for divs in all_divs:
        imgurl = divs["src"];
        img = Image.open(requests.get(imgurl,stream=True).raw);
        img.save(f"{save_directory}/{folder_name} - {i}.jpg","JPEG");
        i+=1;

    driver.close();

## main starting point

driver = webdriver.Chrome("./chromedriver");
driver.get(main_url);

time.sleep(5);

html = driver.page_source;

soup = BeautifulSoup(html,"html.parser");
all_pages = soup.find("ul", class_ = "pagination");

title_array = soup.find("title").text.strip().split("|");

driver.close();

folder_title = title_array[0].strip();

directory = f"{directory}/{folder_title}";
if not os.path.exists(directory):
    os.makedirs(directory);

page_count = count_pages(all_pages);
print(f"Number of pages: {page_count}");

for page in range(page_count):
    print(page+1);

multi_page_scrape(page_count);



#page specific
"""



driver.close();
"""