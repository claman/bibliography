#!/usr/bin/python
import re
file = open('biblio.txt', 'r')

authorSearch = re.compile('^[\D]*\D')
pubDateSearch = re.compile('\d{4}\.')
titleSearch = re.compile('(?<=\d{4}\. )(.*(\."|\. ))')
containingVolumeSearch = re.compile('(?<=( In )).*(?=\d)')

for line in file:
    author = authorSearch.match(line)
    author = author.group().rstrip()
    if author[len(author)-1] == ',':
        author = author[:len(author)-1]

    pubDate = pubDateSearch.search(line)
    pubDate = pubDate.group()
    pubDate = pubDate[:4]

    title = titleSearch.search(line)
    title = title.group()
    split = title.split('.')
    title = split[0]
    if title[0] == '"':
        title = title[1:]
        form = '@article'
    else:
        form = '@book'

    containingVolume = containingVolumeSearch.search(line)
    if containingVolume:
        containingVolume = containingVolume.group()

    print form + '{'
    print ' author: "' + author + '",'
    print ' year: "' + pubDate + '",'
    print ' title: "' + title + '",'
    print '}'
    print
    print containingVolume
