import requests
import constants
import dateutil.parser
import re
from bs4 import BeautifulSoup

# The way njuskalo checks for scrappers are through its headers
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/35.0.1916.47 Safari/537.36'}

page = requests.get(constants.PAGE, headers=HEADERS)
SOUP = BeautifulSoup(page.content, 'html.parser')

if re.findall('Solve the CAPTCHA and come to the dog side!', page.content):
    print "njuskalo has found this as a crawler. Try making less requests, changing headers or just giving up"
    exit(-1)

# The class `EntityList-item` is used through the page so you may be careful searching only for that
# class. That is the reason why we first need to find `EntityList-Regular` where all the latest
# articles are posted
LATEST_ITEMS = (SOUP.find('div', class_='EntityList--Regular')).find_all('li', class_='EntityList-item')

# We gathered all the latest items posted (20 items per page)
# We will grab now only the last item
LATEST_ITEM = LATEST_ITEMS[0]

LATEST_ITEM_TITLE = (LATEST_ITEM.find('h3', class_='entity-title')).find('a')
LATEST_ITEM_SHORT_DESCRIPTION = (LATEST_ITEM.find('div', class_='entity-description-main'))
LATEST_ITEM_POSTED_TIME = dateutil.parser.parse(LATEST_ITEM.find('time')['datetime'])

print "Title: {0}".format(LATEST_ITEM_TITLE.text)
print "Short Description: {0}".format(LATEST_ITEM_SHORT_DESCRIPTION.text.strip())
print "Time Posted: {0}/{1}/{2} {3}:{4}".format(
    LATEST_ITEM_POSTED_TIME.day,
    LATEST_ITEM_POSTED_TIME.month,
    LATEST_ITEM_POSTED_TIME.year,
    LATEST_ITEM_POSTED_TIME.hour,
    LATEST_ITEM_POSTED_TIME.minute
)
print "Link to ad: {0}".format('https://www.njuskalo.hr' + LATEST_ITEM_TITLE['href'])
print "ID ad: {0}".format(LATEST_ITEM_TITLE['name'])
