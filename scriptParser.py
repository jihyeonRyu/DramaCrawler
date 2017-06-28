import re
import requests
from bs4 import BeautifulSoup


def remove_tag(source):
    sTag = re.compile(r'<.*?>[\t\n\r\f\v]*')
    eTag = re.compile(r'[\t\n\r\f\v]*?</.*?>')
    source = sTag.sub("", source)
    source = eTag.sub("", source)
    return source


def get_contents(source):

    xmlPath = BeautifulSoup(source, 'html.parser').find('input', attrs={'name':'xmlPath'})['value']
    g = requests.get(xmlPath)
    soup = BeautifulSoup(g.content, 'lxml')
    title = remove_tag(str(soup.find('volumn_title').find('char')))
    contents = remove_tag(str(soup.find('content', {'id': 'id2'}).find('char'))) + "\n" \
               + remove_tag(str(soup.find('content', {'id': 'id3'}).find('char'))) + "\n" \
               + remove_tag(str(soup.find('content', {'id': 'id4'}).find('char'))) + "\n" \
               + remove_tag(str(soup.find('content', {'id': 'id5'}).find('char'))) + "\n"

    string = soup.find_all('char')

    explain = soup.find_all('scene_explain')
    explain_all = []
    for i in range(len(explain)):
        temp = explain[i].find_all('char')
        for t in temp:
            explain_all.append(t)
    speech = soup.find_all('cast_speech')
    for i in range(len(speech)):
        speech[i] = speech[i].find('char')

    role = soup.find_all('cast_role')
    for i in range(len(role)):
        role[i] = role[i].find('char')

    for s in string:
        if s in explain_all:
            contents = contents + remove_tag(str(s)) + "\n"
        elif s in role:
            contents = contents + remove_tag(str(s)) + ": "
        elif s in speech:
            contents = contents + remove_tag(str(s)) + "\n"
    return title, contents

