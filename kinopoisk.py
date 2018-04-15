import database
import russian_news_classifier
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

BASE_URL = 'https://kingfashion.com/ru/boys-riot-club/'


def get_html(j, driver):
    elem = driver.find_element_by_css_selector("#page_navigator_" + str(j + 1) + "> a")

    elem.send_keys()
    elem.send_keys(Keys.RETURN)
    SCROLL_PAUSE_TIME = 3

    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(5):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver.page_source


def parse_url(cnt):
    j = 1
    driver = webdriver.Firefox(firefox_binary=FirefoxBinary('/home/empire/firefox/firefox'),
                               executable_path='/usr/local/bin/geckodriver')
    driver.get("https://twitter.com/russia")
    many = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
            'у',
            'ф', 'ь', 'ъ', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'э', 'я', 'ю', ' '}
    driver.get("https://www.kinopoisk.ru/reviews/type/comment/period/month/page/1/#list")
    while (j <= cnt):
        html = get_html(j, driver)
        j += 1
        soup = BeautifulSoup(html, 'html.parser')

        neg = soup.findAll("div", "response bad")
        for x in neg:
            name = x.find('p', 'profile_name').get_text()
            text = x.find('span', '_reachbanner_').get_text().replace('\n', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('.', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('?', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('!', ' ')
            text = text.lower()

            res = ""
            for k in range(len(text)):
                if text[k] in many:
                    res += text[k]
            database.new_rec((name,"Горбатая гора", res, russian_news_classifier.predict([res])[0][0]),
                             'usersKINONEG')

        neut = soup.findAll("div", 'response')
        for x in neut:
            name = x.find('p', 'profile_name').get_text()
            text = x.find('span', '_reachbanner_').get_text().replace('\n', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('.', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('?', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('!', ' ')
            text = text.lower()

            res = ""
            for k in range(len(text)):
                if text[k] in many:
                    res += text[k]
            database.new_rec((name, "Горбатая гора", res, russian_news_classifier.predict([res])[0][1]),
                             'usersKINONET')

        pos = soup.findAll("div", 'response good')
        for x in pos:
            name = x.find('p', 'profile_name').get_text()
            text = x.find('span', '_reachbanner_').get_text().replace('\n', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('.', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('?', ' ')
            text = x.find('span', '_reachbanner_').get_text().replace('!', ' ')
            text = text.lower()

            res = ""
            for k in range(len(text)):
                if text[k] in many:
                    res += text[k]
            database.new_rec((name, "Горбатая гора", res, russian_news_classifier.predict([res])[0][2]),
                             'usersKINOPOS')





def main():
    parse_url(5)


if __name__ == '__main__':
    database.createDB()
    main()