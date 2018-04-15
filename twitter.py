import time
import database
import classifier
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

BASE_URL = 'https://kingfashion.com/ru/boys-riot-club/'


def get_html(url, tag, cnt):
    driver = webdriver.Firefox(firefox_binary=FirefoxBinary('/home/empire/firefox/firefox'),
                               executable_path='/usr/local/bin/geckodriver')
    driver.get("https://twitter.com/russia")
    elem = driver.find_element_by_css_selector("#search-query")
    elem.send_keys(tag)
    elem.send_keys(Keys.RETURN)
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

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
    tweets = soup.findAll("p", 'TweetTextSize js-tweet-text tweet-text')
    nicks = soup.findAll("span", 'username u-dir u-textTruncate')
    ind = 1

    for x in tweets:
        text = x.get_text()
        bf = ""
        text = text.lower()
        many = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                'ф', 'ь', 'ъ', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'э', 'я', 'ю', ' '}

        for k in range(len(text)):
            if text[k] in many:
                bf += text[k]

        bf.replace('\n', ' ')
        nick = nicks[ind].get_text()
        print(ind)
        print(bf)
        database.new_rec((nick,bf,classifier.Bayes([bf])[0][1]),'usersTWI')
        ind += 1


def main(tag):
    parse_url(get_html(BASE_URL, tag,5))


if __name__ == '__main__':
    database.createDB()
    main("#книги")
