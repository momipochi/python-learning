import json
from bs4 import BeautifulSoup
import requests
import os.path
import concurrent.futures
import time
import sys
import io
import imghdr

class FunctionalCommand:
    update = ["-u","update"]
    all_folders = ["*","."]
    list_all = ["-l","list"]
    sort_all = ["sort"]

main_url=""
directory=""
if len(sys.argv) >= 3:
    main_url = sys.argv[2]
    directory = sys.argv[1]

json_template = {}
json_template['urls'] = []
downloaded_dirs = []
def get_request(url):
    return requests.get(url)
def close_request(request):
    request.close()
def photo_scrape(url,this_dir):
    r = get_request(url)
    soup = BeautifulSoup(r.text,"html.parser")
    image_entries = soup.find_all("figure", {"class":"figure"})
    title_entires = soup.find("h1", {"class":"h3"})
    title = title_entires.text.strip()
    title = title.replace("/","-")
    close_request(r)
    this_curr_dir = f"{this_dir}{title}"
    with open(f"{this_curr_dir}\\url.txt",'w') as f:
        f.write(url)
    image_urls = []
    img_dirs = []
    i = 1

    downloaded_info = f"{this_dir}\n{title}\n"
    with open(f"{this_dir}url.txt") as f:
        downloaded_info += f.read()
    downloaded_dirs.append(downloaded_info)
    for image in image_entries:
        img_dirs.append(f"{this_curr_dir}\\{title} - {i}.jpg")
        image_urls.append(image.img["src"])
        i+=1
    print(f" Downloading -\t{title}\n")
    try:
        download_image_thread(image_urls,img_dirs)
    except(IOError, SyntaxError) as e:
        print(f"{title} - bad files")
        os.remove(this_curr_dir)
        return
    print(f" Download completed -\t{title}\n")
def album_scrape(url, this_dir):
    time.sleep(2)
    r = get_request(url)
    soup = BeautifulSoup(r.text,"html.parser")
    image_entries = soup.find_all("figure", {"class":"figure"})
    if image_entries is None or len(image_entries) == 0:
        return False
    title_entries = soup.find_all("article",{"class":"container"})
    close_request(r)
    image_urls = []
    i = 0
    for image in image_entries:
        title = title_entries[i].div.h1.text.strip()
        title = title.replace("/","-")
        this_curr_dir = f"{this_dir}{title}"
        i+=1
        if os.path.exists(this_curr_dir):
            continue
        else:
            os.makedirs(this_curr_dir);
        image_urls.append(image.a["href"])
    if len(image_urls) == 0:
        print(f" {this_dir} No urls to scrape\n")
        return True
    print("\tScraping each album\n")
    photo_scrape_thread(image_urls,[this_dir]*len(image_urls))
    return True

def photo_scrape_thread(urls,dir):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(photo_scrape,urls,dir)
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
def update_folder(this_main_url,curr_dir):
    print(curr_dir)
    pages_left = True
    actual_page = 1
    while pages_left:
        print(f" Scraping page- {actual_page}")
        print(f"{this_main_url}/page/{actual_page}")
        pages_left = album_scrape(f"{this_main_url}/page/{actual_page}",curr_dir)
        actual_page+=1
        if main_url == FunctionalCommand.update[0]:
            pages_left = False
    print(f" {curr_dir} Update complete\n")

def update_folder_thread(this_main_url,curr_dir):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(update_folder,this_main_url,curr_dir)

def run(this_main_url):
    r = get_request(this_main_url);
    soup = BeautifulSoup(r.text,"html.parser")
    title_array = soup.find("title").text.strip().split("|");
    folder_title = title_array[0].strip();
    close_request(r)

    dir = os.listdir(directory)

    for x in dir:
        if x in folder_title:
            folder_title = x
        elif folder_title in x:
            folder_title = x
    curr_dir = f"{directory}{folder_title}\\";

    if not os.path.exists(curr_dir):
        os.makedirs(curr_dir);
    url_txt = f"{curr_dir}url.txt"
    if not os.path.exists(url_txt):
        f = open(url_txt,"w+")
        f.write(this_main_url)
        f.close()

    pages_left = True
    actual_page = 1
    while pages_left:
        print(f" Scraping page- {actual_page}")
        print(f" {this_main_url}/page/{actual_page}")
        pages_left = album_scrape(f"{this_main_url}/page/{actual_page}",curr_dir)
        actual_page+=1
    print(f" {curr_dir} Scrape complete")

def initiate_update(this_dir):
    urls = []
    dirs = []
    all_dirs = os.listdir(this_dir)
    for d in all_dirs:
        dir_open = f"{this_dir}{d}\\url.txt"
        
        if not os.path.exists(dir_open):
            continue
        f = open(dir_open,"r")
        urls.append(f.read().strip())
        dirs.append(f"{this_dir}{d}\\")
    if len(urls) == 0:
        print(" Nothing to update in this directory")
        exit()
    update_folder_thread(urls,dirs)
def list_all_folders(dir):
    if os.path.exists(dir):
        ls = os.listdir(dir)
        print(" Current folders - ")
        
        for l in ls:
            url_text = f"{dir}{l}\\url.txt"
            if not os.path.exists(url_text):
                continue
            with open(url_text,'r') as f:
                url = f.read()
                print(f"\t {l} - {url}\n")
def sort_folders(dir):

    urls = []
    dirs = []
    all_dirs = os.listdir(dir)
    for d in all_dirs:
        dir_open = f"{dir}{d}\\url.txt"
        
        if not os.path.exists(dir_open):
            continue
        f = open(dir_open,"r")
        urls.append(f.read().strip())
        dirs.append(f"{dir}{d}\\")
    if len(urls) == 0:
        print("No urls")
        exit()
    sort_folder_thread(urls,dirs)

def sort_folder(url, dir):
    pages_left = True
    pages = 1
    while pages_left:
        r = get_request(f"{url}/page/{pages}")
        soup = BeautifulSoup(r.text,"html.parser")
        image_entries = soup.find_all("figure", {"class":"figure"})
        if image_entries is None or len(image_entries) == 0:
            pages_left = False
        pages+=1
        close_request(r)
    
    while pages != 0:
        r = get_request(f"{url}/page/{pages}")
        soup = BeautifulSoup(r.text,"html.parser")
        image_entries = soup.find_all("figure", {"class":"figure"})
        title_entries = soup.find_all("article",{"class":"container"})
        i = 0
        for image in image_entries:
            title = title_entries[i].div.h1.text.strip()
            title = title.replace("/","-")
            this_curr_dir = f"{dir}{title}\\"
            i+=1
            if os.path.exists(f"{this_curr_dir}url.txt"):
                os.remove(f"{this_curr_dir}url.txt")
            with open(f"{this_curr_dir}url.txt",'w') as f:
                f.write(image.a["href"])
        pages-=1
        close_request(r)
    
    
def replace_title(title):
    t = title
    t = t.replace("@","-")
    t = t.replace("/","-")
    t = t.replace("\\","-")
    t = t.replace("<","-")
    t = t.replace(">","-")
    t = t.replace("\"","-")
    t = t.replace(":","-")
    t = t.replace("?","-")
    t = t.replace("|","-")
    t = t.replace("*","-")
    
def sort_folder_thread(urls,dirs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(sort_folder,urls,dirs)
if main_url in FunctionalCommand.update:
    initiate_update(directory)
    for up in downloaded_dirs:
        print(up)
elif main_url in FunctionalCommand.list_all:
    list_all_folders(directory)
elif main_url in FunctionalCommand.sort_all:
    sort_folders(directory)
else:
    run(main_url)



