import requests
import constants
import dateutil.parser
import re
import os
import time
from bs4 import BeautifulSoup

# The way njuskalo checks for scrappers are through its headers
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/35.0.1916.47 Safari/537.36'}


def check_new_item():
    page = requests.get(constants.PAGE, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    if re.findall('Solve the CAPTCHA and come to the dog side!', page.content):
        raise Exception(
            'njuskalo has found this as a crawler. Try making less requests, changing headers or just giving up')

    # The class `EntityList-item` is used through the page so you may be careful searching only for that
    # class. That is the reason why we first need to find `EntityList-Regular` where all the latest
    # articles are posted
    latest_items = (soup.find('div', class_='EntityList--Regular')).find_all('li', class_='EntityList-item')

    # We gathered all the latest items posted (20 items per page)
    # We will grab now only the last item
    latest_item = latest_items[0]

    latest_item_title = (latest_item.find('h3', class_='entity-title')).find('a')
    latest_item_short_description = (latest_item.find('div', class_='entity-description-main'))
    latest_item_posted_time = dateutil.parser.parse(latest_item.find('time')['datetime'])

    # if the file exists it means it's not the first time we are running the script
    # therefore we need to check the latest ad posted
    if os.path.isfile(constants.FILE_LOCATION + constants.FILE_NAME):
        f = open(constants.FILE_LOCATION + constants.FILE_NAME, 'r')
        last_saved_item_id = f.readline()

        if last_saved_item_id.strip() != latest_item_title['name'].strip():
            print "There is a new item posted"
            os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))

        else:
            print "There's no new item"

    f = open(constants.FILE_LOCATION + constants.FILE_NAME, 'w+')

    # The name attribute in the `a` tag is the id of the ad
    # we will use that id to check the last item posted
    f.write(latest_item_title['name'] + "\n")
    f.write("ID ad: {0}\n".format(latest_item_title['name']))
    f.write("Title: {0}\n".format(latest_item_title.text.encode('utf-8')))
    f.write("Short Description: {0}\n".format(latest_item_short_description.text.encode('utf-8').strip()))
    f.write("Time Posted: {0}/{1}/{2} {3}:{4}\n".format(
        latest_item_posted_time.day,
        latest_item_posted_time.month,
        latest_item_posted_time.year,
        latest_item_posted_time.hour,
        latest_item_posted_time.minute
    ))
    f.write("Link to ad: {0}\n".format('https://www.njuskalo.hr' + latest_item_title['href']))
    f.close()




if __name__ == "__main__":
    while True:
        check_new_item()
        time.sleep(constants.SECONDS_TO_CALL_FUNCTION)
