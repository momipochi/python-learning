import json
from bs4 import BeautifulSoup
import requests
import os.path
import concurrent.futures
import time
import sys

main_url = sys.argv[1]
directory = sys.argv[2]

def count_pages(page_set):
    page_count = 1;
    if not page_set == None:
        pages = page_set.find_all("li");
        
        count_string = pages[len(pages)-2].text;
        
        page_count = int(count_string.replace(",",""))
    return page_count
def get_request(url):
    return requests.get(url)
def close_request(request):
    request.close()
def photo_scrape(url):
    r = get_request(url)
    soup = BeautifulSoup(r.text,"html.parser")
    image_entries = soup.find_all("figure", {"class":"figure"})
    title_entires = soup.find("h1", {"class":"h3"})
    title = title_entires.text.strip()
    close_request(r)
    dir = f"{directory}{title}"
    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir);

    image_urls = []
    img_dirs = []
    i = 1
    for image in image_entries:
        img_dirs.append(f"{dir}\\{title} - {i}.jpg")
        image_urls.append(image.img["src"])
        i+=1
    print(f"\tDownloading - {title}")
    download_image_thread(image_urls,img_dirs)
def album_scrape(url):
    time.sleep(2)
    r = get_request(url)
    soup = BeautifulSoup(r.text,"html.parser")
    image_entries = soup.find_all("figure", {"class":"figure"})
    title_entries = soup.find_all("article",{"class":"container"})
    close_request(r)
    image_urls = []
    i = 0
    for image in image_entries:
        title = title_entries[i].div.h1.text.strip()
        dir = f"{directory}{title}"
        i+=1
        if os.path.exists(dir):
            continue
        image_urls.append(image.a["href"])
    if len(image_urls) == 0:
        print(" No urls to scrape")
        return
    print("\tScraping each album")
    photo_scrape_thread(image_urls)

def photo_scrape_thread(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(photo_scrape,urls)
def download_image(url,dir):
    if os.path.isfile(dir):
        return
    time.sleep(2)
    img_bytes = requests.get(url).content
    with open(dir,'wb') as img_file:
        img_file.write(img_bytes)
def download_image_thread(urls, dirs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image,urls,dirs)




r = get_request(main_url);
soup = BeautifulSoup(r.text,"html.parser")

album_entries = soup.find_all("figure", {"class":"figure"})

pagination = soup.find("ul", class_ = "pagination");

title_array = soup.find("title").text.strip().split("|");
folder_title = title_array[0].strip();
close_request(r)

directory = f"{directory}{folder_title}\\";
if not os.path.exists(directory):
    os.makedirs(directory);

page_count = count_pages(pagination)

for page in range(page_count):
    actual_page = page+1
    print(f" Scraping page- {actual_page}")
    print(f"{main_url}/page/{actual_page}")
    album_scrape(f"{main_url}/page/{actual_page}")
print(" Scrape complete")
# r = get_request("https://www.xinmeitulu.com/photo/cos%e7%a6%8f%e5%88%a9-%e7%99%bd%e9%93%b6-%e6%8a%96s%e5%a7%90%e5%a7%90%ef%bc%88%e4%b8%8b%ef%bc%89");
# soup = BeautifulSoup(r.text,"html.parser")

# album_entries = soup.find_all("figure", {"class":"figure"})
# print(album_entries)
