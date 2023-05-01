import requests
from bs4 import BeautifulSoup
import spacy
from spacy.lang.en import English
from spacy.matcher import Matcher, PhraseMatcher
from spacy.lang.ur import Urdu
import os
import json
import re
import csv
from pympler import asizeof
import time
######
# Crawl news articles for english and urdu
######
lang = 'urdu'
limit = 10000 #urdu
i = 1135 # urdu
total = 2670 #urdu
#2013 24  oct last article found
#limit = 1000  # eng
#i = 178  # eng
#total = 7613  # eng
path_to_file = "/home/ahsan/PycharmProjects/pythonProject/data/articles/" + lang
base_url_eng = "https://www.foxnews.com"
base_url_urdu = "https://www.samaa.tv"
terms_eng = {'instagram': ['insta gram', 'insta-gram'], 'facebook': ['face book', 'face-book'], 'twitter': ['twit-ter']}
terms_urdu = {'انسٹاگرام': ['انسٹا گرام', 'انسٹا-گرام'], 'فیس_بک': ['فیس بک', 'فیس-بک'], 'ٹوئٹر': ['ٹو یٹر', 'ٹویٹر']}
log_eng = log_urdu = "/home/ahsan/Documents/p/university/thesis/article_log/" + lang + "_article_log.csv"


def get_var_name(name): return eval(name)


url_eng = get_var_name('base_url_' + lang) + "/api/article-search?searchBy=tags&values=fox-news%2Ftech%2Ftechnologies" \
                                             "&excludeBy=tags&excludeValues=&size=30&from=" + str(total)
url_urdu = get_var_name('base_url_' + lang) + "/tech/2013-10-26"

url_urdu_log = "/home/ahsan/Documents/p/university/thesis/article_log"
nlp_urdu = Urdu()
nlp_eng = English()
headers = {
    'User-Agent': 'Chrome/63.0.3239.132 QIHU 360SE'
}


def on_match(match, doc, id, matches): return id


matcher = PhraseMatcher(get_var_name('nlp_' + lang).vocab)
for words in get_var_name('terms_' + lang):
    list = [get_var_name('nlp_' + lang)(words)]
    for word in get_var_name('terms_' + lang)[words]:
        list.append(get_var_name('nlp_' + lang)(word))
    matcher.add(words, list, on_match=on_match)


def extract_urdu_articles(url):
    f = requests.get(url, headers=headers)
    soup = BeautifulSoup(f.content, 'lxml')
    body = soup.find('div', {'class': 'w-full md:pl-10'})
    articles = body.findAll('article')

    for article in articles:
        global total
        total += 1
        anchor = article.find('h2', {'class': 'story__title'}).find('a')
        title = get_var_name('nlp_' + lang)(anchor.text.strip())
        date = url.split('tech/')[1]
        old_dt = time.strptime("2013-10-26", "%Y-%m-%d")
        new_dt = time.strptime(date, "%Y-%m-%d")
        if new_dt > old_dt: continue
        if new_dt < time.strptime("2012-01-01", "%Y-%m-%d"): return True
        log(anchor.text.strip(), date, matcher(title))
        if len(matcher(title)) > 0:
            global i
            i += 1
            details = requests.get(anchor['href'], headers=headers)
            story = BeautifulSoup(details.content, 'lxml').find('div', {'class': 'story__content'})
            with open(os.path.join(path_to_file, 'data' + str(i) + '.txt'), 'w') as f:
                f.write(str(title))
                f.write('\n')
                f.write(story.text.strip())
    if i < limit:
        previous = get_var_name('base_url_' + lang) + '/' + body.find('a', {'class': 'cursor-pointer'})['href']
        extract_urdu_articles(previous)

    return True


def extract_eng_articles(url):
    response = requests.get(url)
    if not response:
        print('data is not available')
        return True
    articles = json.loads(response.text)
    print(asizeof.asizeof(articles))

    for article in articles:
        global total
        total += 1
        title = get_var_name('nlp_' + lang)(re.sub('[^a-z0-9.]+', ' ', article['title'].lower()))
        old_dt = time.strptime("2012-01-09", "%Y-%m-%d")
        new_dt = time.strptime(str(article['publicationDate']).split("T")[0], "%Y-%m-%d")
        if new_dt > old_dt: continue
        if new_dt < time.strptime("2012-01-01", "%Y-%m-%d"): exit
        log(article['title'].lower(), str(article['publicationDate']).split("T")[0], matcher(title))
        if len(matcher(title)) > 0:
            global i
            i += 1
            link = get_var_name('base_url_' + lang) + article['url'] if not get_var_name('base_url_' + lang) in article[
                'url'] else article['url']
            details = requests.get(link, headers=headers)
            story = BeautifulSoup(details.content, 'lxml').find('div', {'class': 'article-body'})
            with open(os.path.join(path_to_file, 'data' + str(i) + '.txt'), 'w') as f:
                f.write(str(title))
                f.write('\n')
                if story:
                    f.write(clean_data(story, False if "tech/" not in article['url'] else True).text.lower().strip())
    if i < limit:
        previous = get_var_name('url_' + lang).split('from=')[0] + "from=" + str(total)
        print(previous)
        get_var_name('extract_' + lang + '_articles')(previous)

    return True


def clean_data(story, tech):
    for tag in story.find_all('div', class_='ad-container'):
        tag.decompose()

    c = -1
    elements = -3 if not tech else -3 if tech and not story.find('h2') else -5
    while c > elements:
        story.find_all('p')[-1].decompose()
        c -= 1
    if tech and story.find('h2'):
        story.find_all('h2')[-1].decompose()

    return story


def log(title, date, matches):
    twitter = instagram = facebook = 0
    keys = [*get_var_name('terms_' + lang)]
    if len(matches) > 0:
        for match in matches:
            term = get_var_name('nlp_' + lang).vocab.strings[match[0]]
            if term == keys[0]:
                instagram += 1
            elif term == keys[1]:
                facebook += 1
            elif term == keys[2]:
                twitter += 1

    data = [title, date, twitter, instagram, facebook]
    with open(get_var_name('log_' + lang), 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)


get_var_name('extract_' + lang + '_articles')(get_var_name('url_' + lang))
print("Total Articles :" + str(total))
print("Selected Articles :" + str(i))
