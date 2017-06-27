import re
from bs4 import BeautifulSoup

def removeTag(source):
    sTag = re.compile(r'<.*?>\n')
    eTag = re.compile(r'</.*?>')
    source = sTag.sub("", source)
    source = eTag.sub("", source)
    return source

def getTitle(source):
    soup = BeautifulSoup(source, 'html.parser')
    titles = soup.find_all(id="title")
    for i in range(len(titles)):
        titles[i] = removeTag(str(titles[i]))

    if len(titles) >= 2:
        return ".\\data\\%s_%s.txt" % (titles[0], titles[1])
    else:
        return ".\\data\\%s.txt" % titles[0]


def getContents(source):
    print("+++++++++++++++++++++++++++")
    soup = BeautifulSoup(source)
    print(soup.prettify())
    raw = soup.find_all("tr")
    print(raw)
    contents = ""
    for i in range(len(raw)):
        c = raw[i].find('td', attrs={'id':'left'})
        s = raw[i].find('td', attrs={'id':'right'})
        if c and s is not None:
            contents = contents + "%s :: %s" % (removeTag(str(c)), removeTag(str(s)))

    return contents

    """
    raw = [r for r in driver.find_elements_by_xpath('//tr')]
    contents = ""
    for i in range(len(raw)):
        try:
            c = raw[i].find_element_by_id('left')
            s = raw[i].find_element_by_id('right')
            contents = contents + "%s :: %s" % (removeTag(str(c.text)), removeTag(str(s.text)))
        except:
            continue

    return contents
    """