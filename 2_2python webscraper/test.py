import json
from lxml import html
import requests

page = requests.get('https://www.nicovideo.jp/user/3565926')
data = page.json();
# tree = html.fromstring(page.content)
# #This will create a list of buyers:
# nico = tree.xpath('//div[@class="NicorepoItem-contentDetailLabel"]/text()')

print(data);