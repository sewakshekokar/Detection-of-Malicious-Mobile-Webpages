# A. Code for ML Model
import pandas as pd
import requests  
# import numpy as np
# import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import urllib.request
import pickle
# from math import sqrt, exp, pi
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
# from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Load URLs
with open('feed.txt', 'r') as f:
    malicious_urls = [line.strip() for line in f.readlines()]
with open('legitimate_sites.txt', 'r') as f:
    benign_urls = [line.strip() for line in f.readlines()]

def extract_features(url, label):
    features = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
    except:
        return None

    def count_tag(tag, attr=None):
        if attr:
            return len(soup.find_all(tag, attrs=attr))
        return len(soup.find_all(tag))

    features.extend([
        int(count_tag('script') > 0),
        int(count_tag('noscript') > 0),
        int(count_tag('script', {'src': True}) > 0),
        int(count_tag('script') - count_tag('script', {'src': True}) > 0),
        int(count_tag('img') > 0),
        int(count_tag('iframe') > 0),
        int(count_tag('meta', {'http-equiv': 'Refresh'}) > 0),
        int(len(soup.find_all('a')) > 0)
    ])

    features.extend([
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

    features.extend([sms, tel, apk, mms])
    features.append(len(url))
    features.extend([url.count(c) for c in ['/', '?', '.', '-', '_', '=', '&', ';']])
    features.append(sum(1 for ch in url if ch.isdigit()))

    # Alexa ranks
    try:
        xml = urllib.request.urlopen(f"http://data.alexa.com/data?cli=10&dat=s&url={url}").read()
        soup = BeautifulSoup(xml, "xml")
        features.append(int(soup.find("REACH")["RANK"]))
    except:
        features.append(0)
    try:
        features.append(int(soup.find("COUNTRY")["RANK"]))
    except:
        features.append(0)

    features.append(label)
    return features

# Process all URLs
features_list = []
for url in malicious_urls:
    feat = extract_features(url, 1)
    if feat: features_list.append(feat)
for url in benign_urls:
    feat = extract_features(url, 0)
    if feat: features_list.append(feat)

df = pd.DataFrame(features_list)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
model = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=0)
model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)
print("Random Forest Accuracy:", accuracy_score(y_test, pred))

# Save model
with open('saved_model.pkl', 'wb') as f:
    pickle.dump(model, f, protocol=2)
