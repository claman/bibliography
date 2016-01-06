#!/usr/bin/python
import re

authorSearch = re.compile('^[\D]*\D')
pubDateSearch = re.compile('\d{4}\.')
titleSearch = re.compile('(?<=\d{4}\. )(.*(\."|\. ))')
journalSearch = re.compile('(?<="\s)(.*)(?=:)')
volumeSearch = re.compile('(?<=\D)(\d*)(?=\()')
issueSearch = re.compile('(?<=\()(\d*)(?=\))')
journalPagesSearch = re.compile('(?::\s*)(\d*-\d*)')
containingVolumeInfoSearch = re.compile('(?<=( In ))(.*\d*\.)')
containingVolumeSearch = re.compile('(.*)(?=, \d*-\d*\.)')
publishingInfoSearch = re.compile('(?<=\d{4}\. )(.*)')
publishingInfoExtract = re.compile('(?<=\. )(.*)(?=\.)')

def getAuthor(search):
    author = authorSearch.match(search)
    author = author.group().rstrip()
    if author[len(author)-1] == ',':
        author = author[:len(author)-1]
        return author
    else:
        return author
def getPubDate(search):
    pubDate = pubDateSearch.search(search)
    pubDate = pubDate.group()
    pubDate = pubDate[:4]
    return pubDate
def getTitle(search):
    title = titleSearch.search(search)
    title = title.group()
    split = title.split('.')
    title = split[0]
    return title
def edit(term):
    editedTerm = str(raw_input(term + ': '))
    return editedTerm
