import re
import requests
from bs4 import BeautifulSoup


def remove_tag(source):
    sTag = re.compile(r'<.*?>[\t\n\r\f\v]*')
    eTag = re.compile(r'[\t\n\r\f\v]*?</.*?>')
    source = sTag.sub("", source)
    source = eTag.sub("", source)
    return source


def get_title(source):
    soup = BeautifulSoup(source, 'html.parser')
    titles = soup.find_all(id="title")
    for i in range(len(titles)):
        titles[i] = remove_tag(str(titles[i]))

    if len(titles) >= 2:
        return ".\\data\\%s_%s.txt" % (titles[0], titles[1])
    elif len(titles) == 1:
        return ".\\data\\%s.txt" % titles[0]
    else:
        print("no title")
        return "noTitle"


def get_contents(source):

    xmlPath = BeautifulSoup(source, 'html.parser').find('input', attrs={'name':'xmlPath'})['value']
    r = requests.get(xmlPath)
    soup = BeautifulSoup(r.content, 'lxml')
    raw = soup.find_all('cast')
    contents = ""
    for r in raw:

        roles = r.find_all('cast_role')

        for i in range(len(roles)):
            roles[i] = roles[i].find('char')

        speechs = r.find_all('cast_speech')

        for i in range(len(speechs)):
            speechs[i] = speechs[i].find('char')

        string = r.find_all('char')

        for i in range(len(string)):
            if string[i] in roles:
                contents = contents + remove_tag(str(string[i])) + ": "

            elif string[i] in speechs:
                contents = contents + remove_tag(str(string[i])) + "\n"

    return contents


"""
    all_contents = str(soup.prettify())
    print(all_contents)
    raw = re.findall(
    r'<tr>[ \t\n\r\f\v]*?<td id="left" .*?>[^<]*?</td>[ \t\n\r\f\v]*?<td id="right">[^<]*?</td>[ \t\n\r\f\v]*?</tr>',
    all_contents)
"""
