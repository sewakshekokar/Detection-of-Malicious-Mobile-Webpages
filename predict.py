# B. Code for Classifying the URL
import requests
from bs4 import BeautifulSoup
import urllib.request
import pickle
# import numpy as np

def retrive_pred(URL):
    try:
        r = requests.get(URL, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        print("Failed to fetch URL:", URL)
        print("Error:", e)
        return "Could not fetch URL. Possibly offline or invalid."


    def count_tag(tag, attr=None):
        if attr:
            return len(soup.find_all(tag, attrs=attr))
        return len(soup.find_all(tag))

    temp = []
    temp.extend([
        int(count_tag('script') > 0),
        int(count_tag('noscript') > 0),
        int(count_tag('script', {'src': True}) > 0),
        int(count_tag('script') - count_tag('script', {'src': True}) > 0),
        int(count_tag('img') > 0),
        int(count_tag('iframe') > 0),
        int(count_tag('meta', {'http-equiv': 'Refresh'}) > 0),
        int(len(soup.find_all('a')) > 0)
    ])

    temp.extend([
        count_tag('script'),
        count_tag('noscript'),
        count_tag('script', {'src': True}),
        count_tag('script') - count_tag('script', {'src': True}),
        count_tag('img'),
        count_tag('iframe'),
        count_tag('meta', {'http-equiv': 'Refresh'}),
        len(soup.find_all('a'))
    ])

    sms = tel = apk = mms = 0
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('sms'): sms += 1
        elif href.startswith('tel'): tel += 1
        elif href.endswith('apk'): apk += 1
        elif href.startswith('mms'): mms += 1
    temp.extend([sms, tel, apk, mms])
    temp.append(len(URL))
    temp.extend([URL.count(c) for c in ['/', '?', '.', '-', '_', '=', '&', ';']])
    temp.append(sum(1 for ch in URL if ch.isdigit()))

    try:
        xml = urllib.request.urlopen(f"http://data.alexa.com/data?cli=10&dat=s&url={URL}").read()
        soup = BeautifulSoup(xml, "xml")
        temp.append(int(soup.find("REACH")["RANK"]))
    except:
        temp.append(0)
    try:
        temp.append(int(soup.find("COUNTRY")["RANK"]))
    except:
        temp.append(0)

    model = pickle.load(open('saved_model.pkl', 'rb'))
    result = model.predict([temp])
    return "Malicious" if result[0] == 1 else "Non malicious"
