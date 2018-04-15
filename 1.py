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
import re,csv

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#driver = webdriver.Firefox()
#driver.get("https://twitter.com/search?q=%23books&src=typd")
#elem = driver.find_element_by_css_selector("#search-query")
#elem.send_keys("books")
#r = elem.send_keys(Keys.RETURN)

#search_tag('books')

#r = requests.get('https://twitter.com/search?q=%23books&src=typd')
#reviews = bs4.BeautifulSoup(r.text, 'lxml').findAll("p", 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
#print(len(reviews))
#for r in reviews:
#    print(r, '\n')

BASE_URL = 'https://kingfashion.com/ru/boys-riot-club/'



def get_html(url, tag):
    # req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    # response = urlopen(req).read()
    driver = webdriver.Firefox()
    driver.get("https://twitter.com/russia")
    elem = driver.find_element_by_css_selector("#search-query")
    elem.send_keys(tag)
    elem.send_keys(Keys.RETURN)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    cnt = 400
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
    table = soup.findAll("p", 'TweetTextSize js-tweet-text tweet-text')
    nicks = soup.findAll("span", 'username u-dir u-textTruncate')
    #print(table)
    ind = 1
    fout = open('tweets.txt', 'w', encoding='utf-8')
    for x in table:
        p = re.compile(r'([^a-zA-Z ])')
    #    xtext = x.get_text()

    #    print(xtext, '\n')
        x1 = x.get_text()
        i = x1.find('#')
      #  before_comma = x1[:i] if i != -1 else x1
       # bf = re.sub(r'[\d]|[a-z]|\/', r'', before_comma)
        k = 0
        bf = ""
        x1 = x1.lower()
        many = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'ь', 'ъ', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'э', 'я', 'ю', ' ', '.', '?'}
        while (k < len(x1)):
            if (x1[k] in many):
                bf += x1[k]
            k+=1
        bf.replace('\n', ' ')
        bf = nicks[ind].get_text() + ";" + bf
        fout.write(bf)
        fout.write('\n')
        ind+=1
        #print(type(x))
   # rows = table.find_all("p")
    projects = []
    print(len(table))
    print(len(nicks))
    fout.close()
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
    tag = "#книги"
    all_url = parse_url(get_html(BASE_URL, tag))
    #save_url(all_url, 'url.csv')
    # get_html(BASE_URL)

if __name__ == '__main__':
    main()
