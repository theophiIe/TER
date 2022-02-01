import requests
import re
from bs4 import BeautifulSoup

url = 'https://lessurligneurs.eu/lire/'


def get_nombre_pages(url_page) -> int:
    return int(str(BeautifulSoup(requests.get(url_page + "page/2/").content, 'lxml').find('title')).split(' ')[5])


def liens_articles(url_page):
    content = BeautifulSoup(requests.get(url_page + "page/1/").content, 'lxml').find_all(class_='inside')[1:]

    for links in content:
        for link in links.find_all('a'):
            print(link.get('href'))


def all_liens_article(url_page):
    tab_link = []
    cmpt = get_nombre_pages(url_page)
    for i in range(1, cmpt + 1):
        content = BeautifulSoup(requests.get(url_page + "page/" + str(i)).content, 'lxml').find_all(class_='inside')[1:]
        for links in content:
            for link in links.find_all('a'):
                tab_link.append(link.get('href'))

    return tab_link


def source_article(url_page):
    content = BeautifulSoup(requests.get(all_liens_article(url_page)[1]).content, 'lxml')
    for i in content.find('h2'):
        return i.text.split(',')[0]


def source_article_date(url_page):
    content = BeautifulSoup(requests.get(all_liens_article(url_page)[1]).content, 'lxml')
    for i in content.find('h2'):
        return i.text.split(',')[1]


def auteur_article(url_page):
    content = BeautifulSoup(requests.get(all_liens_article(url_page)[1]).content, 'lxml')
    for p in content.find(class_='auteur'):
        print(p.text.split(","))


def etiquette_article(url_page):
    content = BeautifulSoup(requests.get(all_liens_article(url_page)[1]).content, 'lxml')
    for p in content.find('article').find_all('button'):
        print(p.text)


def contenu_article(url_page):
    contenu = ''
    content = BeautifulSoup(requests.get(all_liens_article(url_page)[1]).content, 'lxml')
    for p in content.find('article').find_all('p'):
        contenu = contenu + " " + p.text

    return contenu


#print(contenu_article(url))
#etiquette_article(url)
#print(source_article(url))
#print(source_article_date(url))
print(auteur_article(url))