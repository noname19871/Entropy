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



def get_html(url):
    driver = webdriver.Firefox()
    driver.get("https://www.kinopoisk.ru/top/")
    elem = driver.find_element_by_css_selector("#top250_place_1 > td:nth-child(2) > a")
    elem.send_keys()
    elem.send_keys(Keys.RETURN)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    cnt = 1
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

def parse_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll("span", '_reachbanner_')
    #print(table)
    for x in table:
        p = re.compile(r'(@[А-Яа-я]+)|([^0-9А-Яа-я-. \t])|(.\d+)')
    #    xtext = x.get_text()

    #    print(xtext, '\n')
        x1 = x.get_text()
        i = x1.find('#')
        before_comma = x1[:i] if i != -1 else x1
        bf = re.sub(r'[\d]|[a-z]|\/', r'', before_comma)
        print(bf, '\n')
        #print(type(x))
   # rows = table.find_all("p")
    projects = []
    print(len(table))
  #  for row in rows:
  #      cols = row.find_all('p')
  #      projects.append({
 #           'title': cols[0].text,
 #           'url': cols[0].a['href']
#       })
    return projects

def save_url(projects,path):
    with open(path,'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(('Название', 'URL'))
        writer.writerows(
            (project['title'],project['url']) for project in projects
        )
        csvfile.close()



def main():
    # tag = "#книги"
    all_url = parse_url(get_html(BASE_URL))
    #conn = sqlite3.connect("mydatabase.db")
   # cursor = conn.cursor()

    # Создание таблицы

  #  x = "sdf"
    #cursor.execute("insert into Tweets([tweet]) values (tweet) ")
    #cursor.execute("SELECT * FROM Tweets")

    # Получаем результат сделанного запроса
   # results = cursor.fetchall()

   # print(results)
  #  conn.close()
    #save_url(all_url, 'url.csv')
    # get_html(BASE_URL)

if __name__ == '__main__':
    main()