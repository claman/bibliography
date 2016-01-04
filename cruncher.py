#!/usr/bin/python
import re
file = open('biblio.txt', 'r')

authorSearch = re.compile('^[\D]*\D')
pubDateSearch = re.compile('\d{4}\.')
titleSearch = re.compile('(?<=\d{4}\. )(.*(\."|\. ))')

journalSearch = re.compile('(?<="\s)(.*)(?=:)')
volumeSearch = re.compile('(?<=\D)(\d*)(?=\()')
issueSearch = re.compile('(?<=\()(\d*)(?=\))')
journalPagesSearch = re.compile('(?::\s*)(\d*-\d*)')

# containingVolumeSearch = re.compile('(?<=( In )).*(?=\d)')
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
        format = 'excerpt'
    elif title[0] != '"':
        format = '@book'

    if format == 'excerpt':
        journalPages = journalPagesSearch.search(line)
        # containingVolume = containingVolumeSearch.search(line)
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
        # elif containingVolume:
        #     containingVolume = containingVolume.group()
        #     format = '@section'

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
        if volumeNum:
            print ' volume: "' + volume + '",'
        if issueNum:
            print ' issue: "' + issue + '",'
        print ' pages: "' + pages + '"'
        print '}'
        print
    # elif format == '@section':
    #     print format + '{'
    #     print ' author: "' + author + '",'
    #     print ' year: "' + pubDate + '",'
    #     print ' title: "' + title + '",'
    #     print '}'
    #     print
    #     print containingVolume
