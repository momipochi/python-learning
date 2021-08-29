from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import sys
import concurrent.futures
"""
    sample urls
    https://www.xinmeitulu.com/mote/ninjaazhaizhai
    https://www.xinmeitulu.com/mote/baiyin81
    https://www.xinmeitulu.com/mote/coserxiaocangqiandaiw
    https://www.xinmeitulu.com/mote/chunmomo
    https://tw.xinmeitulu.com/mote/cosermizhimaoqiu
    https://tw.xinmeitulu.com/mote/coseryanjiangdamowangw

"""

scraper_ethics = True;
if not len(sys.argv) > 3:
    scraper_ethics = sys.argv[3];

main_url = sys.argv[1];
print(main_url);
# enter the url you want, make sure the ending does not have page number

directory = sys.argv[2]; # modify this to change directory

chrome_options = Options();
chrome_options.add_argument("--headless");
chrome_options.add_argument("log-level=3");

def count_pages(page_set):
    page_count = 1;
    if not page_set == None:
        pages = page_set.find_all("li");
        
        page_count = int(pages[len(pages)-2].text);
            
    return page_count;
def tabbed_log(str):
    print(f"\t{str}");
def single_page_scrape(driver):
    html = driver.page_source;
    soup = BeautifulSoup(html,"html.parser");
    all_figures = soup.find_all("figure", class_ = "figure");
    all_url = [];
    for figure_url in all_figures:
        all_url.append(figure_url.a["href"]);
        # print(href_link);
    driver.close();
    album_drivers = [];

    for href_link in all_url:
        album_drivers.append(get_page_driver(href_link));
    threaded_page_scrape(album_drivers);
    if scraper_ethics:
        time.sleep(3);

def get_page_driver(url):
    tabbed_log("Getting page driver");
    driver = webdriver.Chrome("./chromedriver",options=chrome_options);
    driver.get(url);
    
    time.sleep(5);
    return driver;

def multi_page_scrape(page_count):
    for page_number in range(page_count):
        print(f"Page {page_number+1}");
        
        page_driver = get_page_driver(f"{main_url}/page/{page_number+1}");

        single_page_scrape(page_driver);

def threaded_page_scrape(album_drivers):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape_page_and_save, album_drivers);

def scrape_page_and_save(driver):
    html = driver.page_source;
    soup = BeautifulSoup(html,"html.parser");

    all_divs = soup.find_all("img", class_ = "figure-img img-fluid rounded");

    title_content = soup.find("h1", class_ = "h3");

    folder_name = title_content.text.strip();


    save_directory = f"{directory}\{folder_name}";

    tabbed_log(f"Save directory- {save_directory}");

    if not os.path.exists(save_directory):
        os.makedirs(save_directory);
    else:
        return;
    i = 1;

    img_urls = [];
    img_dirs = []
    for divs in all_divs:
        img_urls.append(divs["src"]);
        img_dirs.append(f"{save_directory}\{folder_name} - {i}.jpg");
        i+=1;
    driver.close();
    tabbed_log("Downloading images..");
    if scraper_ethics:
        time.sleep(3);
    threadDownload(img_urls,img_dirs);

def downloadImage(img_url,img_dir):
    if scraper_ethics:
        time.sleep(1);
    img_bytes = requests.get(img_url).content;
    with open(img_dir, 'wb') as img_file:
        img_file.write(img_bytes);

def threadDownload(img_urls, img_dirs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(downloadImage, img_urls,img_dirs);

## main starting point

driver = get_page_driver(main_url);

html = driver.page_source;

soup = BeautifulSoup(html,"html.parser");
all_pages = soup.find("ul", class_ = "pagination");

title_array = soup.find("title").text.strip().split("|");

driver.close();

folder_title = title_array[0].strip();

directory = f"{directory}{folder_title}";
if not os.path.exists(directory):
    os.makedirs(directory);

page_count = count_pages(all_pages);
print(f"Number of pages: {page_count}");


multi_page_scrape(page_count);

