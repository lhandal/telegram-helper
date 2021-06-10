import unicodedata
import requests
import re
import bs4
from random import randint
from bs4 import BeautifulSoup
from libgen_api import LibgenSearch




def normalize_text(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text).lower()

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def gangstarize(input_text: str) -> str:
    params = {"translatetext": input_text}
    target_url = "http://www.gizoogle.net/textilizer.php"
    resp = requests.post(target_url, data=params)
    # the html returned is in poor form normally.
    soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text)
    soup = bs4.BeautifulSoup(soup_input, "lxml")
    giz = soup.find_all(text=True)
    giz_text = giz[37].strip("\r\n")  # Hacky, but consistent.
    return giz_text

def search_book(by, value):
    s = LibgenSearch()
    if by == 'title':
        results = s.search_title(value)
    elif by == 'author':
        results = s.search_author(value)
    return results

def filter_results(search_results):
    filtered_results = []
    try:
        wanted_keys = list(search_results[0].keys())[1:9]
        for i in range(len(search_results)):
            filtered_results.append({k: v for k, v in search_results[i].items() if k in wanted_keys})
    except IndexError:
        pass
    return filtered_results

def get_book_link(user_pick):
    if user_pick['Mirror_1']:
        r = requests.get(user_pick['Mirror_1'])
    elif not user_pick['Mirror_1']:
        r = requests.get('http://libgen.lc/' + user_pick['Mirror_2'])
    soup = BeautifulSoup(r.content, features="lxml")
    url = soup.find('a', href=True)['href']
    return url

def get_roast():
    if randint(0,3) == 0:
        url ='http://private-anon-3c099af7c5-insultgenerator.apiary-mock.com/compliments'
        const = 'compliments'
        emoji = '😍'
    else:
        url ='http://private-anon-3c099af7c5-insultgenerator.apiary-mock.com/insults'
        const = 'insults'
        emoji = '😂'
    results = requests.get(url).json()
    try:
        roast = results[randint(0,len(results))][const][0][const[:-1]+'_no_name'].lower()+'! '+emoji
    except:
        roast = results[randint(0,len(results))][const][0][const[:-1]+'_no_name'].lower()+'! '+emoji
    return roast