#!/usr/bin/python
import re
file = open('biblio.txt', 'r')
output = open('output.bib', 'w')

authorSearch = re.compile('^[\D]*\D')
pubDateSearch = re.compile('\d{4}\.')
titleSearch = re.compile('(?<=\d{4}\. )(.*(\."|\. ))')

journalSearch = re.compile('(?<="\s)(.*)(?=:)')
volumeSearch = re.compile('(?<=\D)(\d*)(?=\()')
issueSearch = re.compile('(?<=\()(\d*)(?=\))')
journalPagesSearch = re.compile('(?::\s*)(\d*-\d*)')

containingVolumeInfoSearch = re.compile('(?<=( In ))(.*\d*\.)')
containingVolumeSearch = re.compile('(.*)(?=, \d*-\d*\.)')

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
        format = 'excerpt'
    elif title[0] != '"':
        format = '@book'

    if format == 'excerpt':
        journalPages = journalPagesSearch.search(line)
        containingVolumeInfo = containingVolumeInfoSearch.search(line)
        if journalPages:
            format = '@article'
            journal = journalSearch.search(line).group()
            volumeNum = volumeSearch.search(journal)
            issueNum = issueSearch.search(journal)
            if volumeNum:
                volume = volumeNum.group()
            if issueNum:
                issue = issueNum.group()
            pages = re.search('(\d*-\d*)', journalPages.group()).group()
        elif containingVolumeInfo:
            format = '@section'
            bookInfo = re.search('(.*\d\.)', containingVolumeInfo.group()).group()
            pages = re.search('(\d*-\d*)(?=\.)', bookInfo).group()
            bookTitle = containingVolumeSearch.search(bookInfo).group()

    if format == '@book':
        print format + '{'
        print ' author: "' + author + '",'
        print ' year: "' + pubDate + '",'
        print ' title: "' + title + '",'
        print '}'
        print
    elif format == '@article':
        print format + '{'
        print ' author: "' + author + '",'
        print ' year: "' + pubDate + '",'
        print ' title: "' + title + '",'
        print ' journal: "' + journal + '",'
        if volumeNum:
            print ' volume: "' + volume + '",'
        if issueNum:
            print ' issue: "' + issue + '",'
        print ' pages: "' + pages + '"'
        print '}'
        print
    elif format == '@section':
        print format + '{'
        print ' author: "' + author + '",'
        print ' year: "' + pubDate + '",'
        print ' title: "' + title + '",'
        print ' book: "' + bookTitle + '",'
        print ' pages: "' + pages + '"'
        print '}'
        print

file.close()
