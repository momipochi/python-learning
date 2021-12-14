import time
import requests
import json
import os.path
import sys
import concurrent.futures
from bs4 import BeautifulSoup


def download_image_thread(img_urls, img_dirs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, img_urls,img_dirs)

def download_image(img_url,img_dir):
    if os.path.isfile(img_dir):
        return
    time.sleep(2)
    img_bytes = requests.get(img_url).content
    with open(img_dir, 'wb') as img_file:
        img_file.write(img_bytes)


main_url = sys.argv[2]
ehentai_login = "https://forums.e-hentai.org/index.php?act=Login&CODE=01"
main_site = "https://nhentai.net"
login_data = {
    'referer': 'https://www.google.com/',
    'b': '',
    'bt': '',
    'UserName': 'cheapflight',
    'PassWord': '2nunsarehot',
    'CookieDate': '1'
}

payload = {
    'Connection': 'close',
    'Cookie': 'ipb_member_id=4872233; ipb_pass_hash=3c7affc6aeba7ca114a67b617925b937; igneous=7722c34fc; sl=dm_1; sk=cpxprbvsbstbemk35d1a83mpx7sk',
    'Host': 'exhentai.org'
}

payloadNhen = {
    'authority': 'nhentai.net',
    'method': 'GET',
    'path': '/g/370420/',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,la;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'csrftoken=HVA9HRvJsPvfMxHXnieMqFWgwy9OUJDuRmKkVgJyPYrMo9bckexnM9hw4EZdJLsD; sessionid=5mx0ax1rpskph42do4voqahtwjny9cjn',
    'referer': 'https://nhentai.net/search/?q=hizuki+akira',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

proxyDict = {
                "proxyAddress": "127.0.0.1",
                "proxyPort": "7890"
            }

headers = {'content-type': 'applicaiton/json'}

# r = requests.post(ehentai_login,data=login_data)

r = requests.get(main_url)
soup = BeautifulSoup(r.text,'html.parser')
tags = soup.find_all("div",{"class": "tag-container field-name"})
titles = soup.find_all("h2",{"class": "title"})
r.close()

folder_title= ""
for title in titles:
    folder_title = f"{folder_title} {title.text}"
folder_title = folder_title.strip()
print(folder_title)
page = ""
artist = ""
artist_url =[]
group_url =[]
for tag in tags:
    if "Groups:" in tag.text:
        group = tag.a["href"]
        group_url = f"{main_site}{group}"
    if "Artists:" in tag.text:
        artist = tag.a.span.text.strip()
        artist_href = tag.a["href"]
        artist_url = f"{main_site}{artist_href}"
    if "Pages:" in tag.text:
        page = tag.text

print(artist)
page_arr = page.split("\t")
page_num = int(page_arr[len(page_arr)-1])
print(page_num)

page_num +=1


directory = sys.argv[1]
dir = f"{directory}{artist}\\"
if not os.path.exists(dir):
    os.makedirs(dir);
if not os.path.exists(f"{dir}url.txt"):
    f = open(f"{dir}url.txt","w+")
    f.write(f"Artist- {artist_url}\n")
    f.write(f"Group- {group_url}")
    f.close()

dir = f"{dir}{folder_title}\\"

# print(dir)
if not os.path.exists(dir):
    os.makedirs(dir);
else:
    if not os.path.exists(f"{dir}url.txt"):
        f = open(f"{dir}url.txt","w+")
        f.write(main_url)
        f.close()
    exit()
if not os.path.exists(f"{dir}url.txt"):
    f = open(f"{dir}url.txt","w+")
    f.write(main_url)
    f.close()
img_urls = []
img_dirs = []

print("getting all urls")
for i in range(page_num-1):
    url = f"{main_url}{i+1}/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    photo_link = soup.findAll("section",{"id": "image-container"})
    # print("--")
    # print(i+1)
    # print(photo_link)
    # print(url)
    link = photo_link[0].a.img["src"]
    # download_image(link,f"{dir}{folder_title} - {i}.jpg")
    # if i%4 == 0:
    #     time.sleep(2)
    img_urls.append(link)
    img_dirs.append(f"{dir}{folder_title} - {i+1}.jpg")
r.close()
print("starting download")
download_image_thread(img_urls,img_dirs)
print("download completed")



# photo_dirs = []

# for i in range(number_of_photos):
#     photo_dirs.append(f"{directory}\\{i}")
