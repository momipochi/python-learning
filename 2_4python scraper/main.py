from bs4 import BeautifulSoup
import requests
import os.path
import concurrent.futures
import time
import sys
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

fake_captcha_url = "https://www.google.com/recaptcha/api2/demo"

v2_login_url = "https://www.v2ph.com/login?hl=zh-Hans"
v2site_key = "6Ld-qt8UAAAAAOHRX8h9XyZno6LA6653tOgQhkaB"
info = ["havesome96@gmail.com","Havesome96"]
payload = {
    "email": "havesome96@gmail.com",
    "password": "Havesome96",
    "g-recaptcha-response": "03AGdBq26OrvzgDRUwELw_O0u_e2HqwtC-WwqTLkNWyLPVk4ppKxML5quiJD8ZJ_KNzbt6BOmopOdLewWaJixvPn_ZWUUE1w0b_AM-B5KlupTLc4uQUwnu9e8tND4mVE6kz2z9VasESHxhKLuWkt_7mBGV1C3CutiHtKQP422tW9AVqkX188v_Ys0tzk4MUQyo6wcg-8RrL1hudk_a6wLJmyhbW9cj0eLzpPE3hE7JiUemiD9dMi1o6PjQ1JoGSOefBR-x2V7n9kwRbS6QIhHwfJKxftisSXvB_GZCdnTq_9R2TQzXNv-AdD1eJjvUgw9ZK8LkE0HrgkH47drEVQDP1og6FH7LYMIagrWjagXOfm7L4UbB-77fzq1Xk1GxT6LhSb1tEHmc1bX8LcGBlbrqGjcLSXhocIpv0MiKuNdeE2G4LUtRlL7HRaa8q9aO050IApTkR-Gl8xhJ",
    "remember": "1"
}
captcha_payload = {
    
}
request_header = {
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-GB,en-US;q=0.9,en;q=0.8,la;q=0.7",
"cache-control": "max-age=0",
"cookie": "frontend=9b2cb43027565ee949287b0f0a76b654; _gid=GA1.2.921067943.1630409513; frontend-rmu=YnhGZ4G14xRliV9onIN3rdFoo61D; frontend-rmt=cXMAudiAjwBa7gMbVVz7LlZ9D8f6tWGrOOJeEd1URkwVyUI9wrVscj15R8yR6lpy; _gat_UA-140713725-1=1; __cf_bm=88af22804a737196cee51ff562c8c5d485c0bcbe-1630420851-1800-Aa/oRzFL0bOmnnJqsj9Qu4LW8UGbd2FNEe77/+xkaTaQuaDbiUQV7fE3epKiAGzhel7Wd3leiPuNdBOrEKRPrfkX9p2v4rrzcEa3A+5DnUIKlMsYu81EZHFBZp0pf2NJAA==; _ga_170M3FX3HZ=GS1.1.1630418700.2.1.1630420854.53; _ga=GA1.2.1729187268.1630409513",
"sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
"sec-ch-ua-mobile": "?0",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

# main_url = sys.argv[2]
# directory = sys.argv[1]

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

def photo_books_scrape(url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    photo_book_url = soup.find_all("a", class_ = "media-cover")
    each_book_url = []
    i = 0
    for book_url in photo_book_url:
        href = book_url["href"].strip()
        each_book_url.append(f"{main_web}{href}")
    print(f" Photo books- {len(each_book_url)}")
    print(each_book_url[0])
    book_scrape(each_book_url[0])
    r.close()
    
def book_scrape(url):
    global directory
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    title = soup.find("h1", class_="h5 text-center mb-3").text
    dir = f"{directory}{title}\\"
    print(title)
    r.close()
    if not os.path.exists(dir):
        os.makedirs(dir);
    if not os.path.exists(f"{dir}v2url.txt"):
        f = open(f"{dir}v2url.txt","w+")
        f.write(url)
        f.close()
    tmp_url = url.split("?")
    main_url_head = tmp_url[0].strip()
    main_url_tail = tmp_url[1].strip()
    page_remain = True
    index = 1
    each_photo_url = []
    each_photo_dir = []
    dir_num = 1
    while page_remain:
        url = f"{main_url_head}?page={index}&{main_url_tail}"
        print(url)
        driver = webdriver.Chrome("./chromedriver",options=chrome_options)
        # s = requests.Session()
        # s.get(url,data=payload)
        # s.post(url,data=payload)
        # r = s.get(url)
        # print(r)
        driver.get(url)
        email = driver.find_element_by_id("email")
        password = driver.find_element_by_id("password")
        
        email.send_keys(info[0])
        password.send_keys(info[0])

        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        print(soup)
        photo_url = soup.find_all("div",class_="album-photo my-2")
        print(photo_url)
        return
        for p in photo_url:
            print(p)
            each_photo_url.append(p.img["data-src"])
            each_photo_dir.append(f"{dir}{title} - {dir_num}")
            dir_num+=1
        print(each_photo_url[0])
        print(len(each_photo_url))
        print(each_photo_dir[0])
        print(len(each_photo_dir))
        r.close()

        index+=1
    
directory = "D:\\csp\\irl ref\\" 
main_web = "https://www.v2ph.com"
main_url = "https://www.v2ph.com/actor/nm34a376.html?hl=zh-Hans"

def run():
    global main_url
    global directory
    
    r = requests.get(main_url);
    soup = BeautifulSoup(r.text,"html.parser")
    # print(soup)

    title = soup.find_all("h1", class_= "h5 text-center text-md-left mt-3 mt-md-0")

    titles = title[0].text.split("、")
    print(titles)
    r.close()

    folder_list = os.listdir(directory)
    dir_title=titles[0].strip()
    dir_exists = False
    i = 0

    if len(titles) > 1:
        print(" Checking if title exists in directory")
        for t in titles:
            t = t.strip()
            print(i)
            for f in folder_list:
                if t == f:
                    dir_title = f
                    dir_exists = True
                    break
            if dir_exists:
                print(" Directory exists")
                break
    else:
        dir_title = titles[0]

    directory = f"{directory}{dir_title}\\"
    print(directory)

    if not os.path.exists(directory):
        os.makedirs(directory);
    url_txt = f"{directory}v2url.txt"
    if not os.path.exists(url_txt):
        f = open(url_txt,"w+")
        f.write(main_url)
        f.close()

    tmp_main_url = main_url.split("?")
    main_url_start = tmp_main_url[0]
    main_url_end = tmp_main_url[1]
    print(tmp_main_url)
    pages_remain = True
    i = 1
    while pages_remain:
        photo_books_url = f"{main_url_start}?page={i}&{main_url_end}"
        photo_books_scrape(photo_books_url)
        pages_remain = False
        i+=1

run()
# https://www.v2ph.com/actor/Barbie?{page=i}&hl=en
# https://www.v2ph.com/actor/Barbie?hl=en
# https://www.v2ph.com/actor/Barbie?page=2&hl=en


# https://www.v2ph.com/album/z46xo6xz.html?hl=zh-Hans
# https://www.v2ph.com/album/z46xo6xz.html?page=2&hl=zh-Hans
# https://www.v2ph.com/actor/nm34a376.html?hl=zh-Hans
# https://www.v2ph.com/actor/nm34a376.html?page=2&hl=zh-Hans
