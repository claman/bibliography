#!/usr/bin/python
import re
file = open('biblio.txt', 'r')

authorSearch = re.compile('^[\D]*\D')
pubDateSearch = re.compile('\d{4}\.')
titleSearch = re.compile('(?<=\d{4}\. )(.*(\."|\. ))')
journalTitleSearch = re.compile('(?<="\s)(.*)(?=:)')
journalPagesSearch = re.compile('(?:\:\s*)(\d*-\d*)')
containingVolumeSearch = re.compile('(?<=( In )).*(?=\d)')
    # for this pull out the pages at the end \d*-\d*\.

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
    elif title[0] != '"':
        format = '@book'
    # if title[0] != '"':
    #     format = '@book'
    # else:
    #     title = title[1:]
    #     switcher = 'true'

    # if switcher == 'true':
    #     journalPages = journalPagesSearch.search(line)
    #     containingVolume = containingVolumeSearch.search(line)
    #     if journalPages:
    #         journal = journalTitleSearch.search(line)
    #         journal = journal.group()
    #         pages = journalPages
    #         format = '@article'
    #     elif containingVolume:
    #         containingVolume = containingVolume.group()
    #         format = '@excerpt'

    if format == '@book':
        print format + '{'
        print ' author: "' + author + '",'
        print ' year: "' + pubDate + '",'
        print ' title: "' + title + '",'
        print '}'
        print
    if format == '@article':
        print format + '{'
        print ' author: "' + author + '",'
        print ' year: "' + pubDate + '",'
        print ' title: "' + title + '",'
        print ' journal: "' + journal + '",'
        print ' pages: "' + pages + '"'
        print '}'
        print
    # elif format == '@excerpt':
    #     print format + '{'
    #     print ' author: "' + author + '",'
    #     print ' year: "' + pubDate + '",'
    #     print ' title: "' + title + '",'
    #     print '}'
    #     print
    #     print containingVolume
