import pandas as pd
import numpy as np
import bs4
import requests
import time
import sys
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from grab import Grab
from urllib.request import Request, urlopen
import re, csv
import sqlite3

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

BASE_URL = 'https://kingfashion.com/ru/boys-riot-club/'


def get_html(url, j, driver):
    # driver = webdriver.Firefox()

    # driver.get("https://www.kinopoisk.ru/top/")
    elem = driver.find_element_by_css_selector("#page_navigator_" + str(j + 1) + "> a")

    elem.send_keys()
    elem.send_keys(Keys.RETURN)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    cnt = 5
    while cnt > 0:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        cnt = cnt - 1
    return driver.page_source


def parse_url():
    j = 1
    driver = webdriver.Firefox()

    driver.get("https://www.kinopoisk.ru/reviews/type/comment/period/month/page/1/#list")
    while (j <= 299):
        html = get_html(BASE_URL, j, driver)
        j += 1
        fn = open('neg.txt', 'a')
        soup = BeautifulSoup(html, 'html.parser')
        neg = soup.findAll("div", "response bad")
        for x in neg:
            fn.write(x.find('p', 'profile_name').get_text())
            fn.write(";")
            fn.write(x.find('span', '_reachbanner_').get_text().replace('\n', ' '))
            fn.write('\n\n\n')

        projects = []
        fn.close()

        fp = open('pos.txt', 'a')
        pos = soup.findAll("div", 'response good')
        # print(table)

        for x in pos:
            fp.write(x.find('p', 'profile_name').get_text())
            fp.write(";")
            fp.write(x.find('span', '_reachbanner_').get_text().replace('\n', ' '))
            fp.write('\n\n\n')

        fp.close()

        fneut = open('neut.txt', 'a')
        neut = soup.findAll("div", 'response')
        # print(table)

        for x in neut:
            fneut.write(x.find('p', 'profile_name').get_text())
            fneut.write(";")
            fneut.write(x.find('span', '_reachbanner_').get_text().replace('\n', ' '))
            fneut.write('\n\n\n')

        fneut.close()
    return projects


def save_url(projects, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(('Название', 'URL'))
        writer.writerows(
            (project['title'], project['url']) for project in projects
        )
        csvfile.close()


def main():
    all_url = parse_url()


if __name__ == '__main__':
    main()