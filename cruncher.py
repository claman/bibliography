#!/usr/bin/python
import re
from functions import getAuthor, getPubDate, getTitle, edit

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
publishingInfoSearch = re.compile('(?<=\d{4}\. )(.*)')
publishingInfoExtract = re.compile('(?<=\. )(.*)(?=\.)')

options = ('y', 's', 'e')
positive = ('y', 'yep', 'yes', 'yeah')
negative = ('n', 'no', 'nop', 'nope')

with open('biblio.txt', 'r') as file:
    for line in file:
        author = getAuthor(line)
        pubDate = getPubDate(line)
        title = getTitle(line)

        if title[0] == '"':
            title = title[1:]
            format = 'excerpt'
        elif title[0] != '"':
            format = '@book'

        if format == '@book':
            publishingInfo = publishingInfoSearch.search(line).group()
            pubExtract = publishingInfoExtract.search(publishingInfo).group()
            pubExtract = pubExtract.split(': ')
            publisher = pubExtract[1]
            publishedCity = pubExtract[0]
        elif format == 'excerpt':
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
                if volumeNum or issueNum:
                    journal = re.search('(\D*)(?=\s(\d|\())', journal).group()
            elif containingVolumeInfo:
                format = '@section'
                bookInfo = re.search('(.*\d\.)',
                  containingVolumeInfo.group()).group()
                pages = re.search('(\d*-\d*)(?=\.)', bookInfo).group()
                bookTitle = containingVolumeSearch.search(bookInfo).group()
                publishingInfo = publishingInfoSearch.search(line).group()
                pubExtract = publishingInfoExtract.search(
                  publishingInfo).group()
                pubExtract = pubExtract.split(': ')
                publisher = pubExtract[1]
                publishedCity = pubExtract[0]

        authorLast = author.split(',')[0].lower()
        titleFirst = title.split(' ')[0].lower()
        citekey = authorLast + pubDate + titleFirst

        print '---'
        print line + '---'
        if format == '@book':
            print 'format: ' + format
            print 'author: ' + author
            print 'year: ' + pubDate
            print 'title: ' + title
            print 'publisher: ' + publisher
            print 'city: ' + publishedCity
            print
        elif format == '@article':
            print format + '{'
            print 'author: "' + author + '",'
            print 'year: "' + pubDate + '",'
            print 'title: "' + title + '",'
            print 'journal: "' + journal + '",'
            if volumeNum:
                print 'volume: "' + volume + '",'
            if issueNum:
                print 'issue: "' + issue + '",'
            print 'pages: "' + pages + '"'
            print '}'
            print
        elif format == '@section':
            print format + '{'
            print 'author: "' + author + '",'
            print 'year: "' + pubDate + '",'
            print 'title: "' + title + '",'
            print 'book: "' + bookTitle + '",'
            print 'pages: "' + pages + '"'
            print 'publisher: ' + publisher
            print 'city: ' + publishedCity
            print '}'
            print

        prompt = str(raw_input("Add entry to bibliography? ([y]es/[s]kip/[e]dit): "))
        if prompt in options:
            if prompt in positive:
                if format == '@book':
                    output.write(format + '{' + citekey + ',\n')
                    output.write(' author = "' + author + '",\n')
                    output.write(' year = "' + pubDate + '",\n')
                    output.write(' title = "' + title + '",\n')
                    output.write(' publisher = "' + publisher + '",\n')
                    output.write(' publishedCity = "' + publishedCity + '",\n')
                    output.write('}\n')
                    output.write('\n')
                elif format == '@article':
                    output.write(format + '{' + citekey + ',\n')
                    output.write(' author = "' + author + '",\n')
                    output.write(' year = "' + pubDate + '",\n')
                    output.write(' title = "' + title + '",\n')
                    output.write(' journal = "' + journal + '",\n')
                    if volumeNum:
                        output.write(' volume = "' + volume + '",\n')
                    if issueNum:
                        output.write(' issue = "' + issue + '",\n')
                    output.write(' pages = "' + pages + '"\n')
                    output.write('}\n')
                    output.write('\n')
                elif format == '@section':
                    output.write(format + '{' + citekey + ',\n')
                    output.write(' author = "' + author + '",\n')
                    output.write(' year = "' + pubDate + '",\n')
                    output.write(' title = "' + title + '",\n')
                    output.write(' book = "' + bookTitle + '",\n')
                    output.write(' pages = "' + pages + '"\n')
                    output.write(' publisher = "' + publisher + '",\n')
                    output.write(' publishedCity = "' + publishedCity + '",\n')
                    output.write('}\n')
                    output.write('\n')
            elif prompt in negative:
                print 'Skipping\n'
                print
            elif prompt[0] == 'e':
                format = str(raw_input('Enter citation format (book, article, or section): '))
                if format == 'book':
                    output.write(format + '{' + edit('citekey') + ',\n')
                    output.write(' author = "' + edit('author') + '",\n')
                    output.write(' year = "' + edit('pubDate') + '",\n')
                    output.write(' title = "' + edit('title') + '",\n')
                    output.write(' publisher = "' + edit('publisher') + '",\n')
                    output.write(' publishedCity = "' + edit('publishedCity') + '",\n')
                    output.write('}\n')
                    output.write('\n')
                elif format == 'article':
                    output.write(format + '{' + edit('citekey') + ',\n')
                    output.write(' author = "' + edit('author') + '",\n')
                    output.write(' year = "' + edit('pubDate') + '",\n')
                    output.write(' title = "' + edit('title') + '",\n')
                    output.write(' journal = "' + edit('journal') + '",\n')
                    volumePrompt = str(raw_input('Specific volume (y/n): '))
                    if volumePrompt == 'y':
                        output.write(' volume = "' + edit('volume') + '",\n')
                    issuePrompt = str(raw_input('Specific issue (y/n): '))
                    if issuePrompt == 'y':
                        output.write(' issue = "' + edit('issue') + '",\n')
                    output.write(' pages = "' + edit('pages') + '"\n')
                    output.write('}\n')
                    output.write('\n')
                elif format == 'section':
                    output.write(format + '{' + edit('citekey') + ',\n')
                    output.write(' author = "' + edit('author') + '",\n')
                    output.write(' year = "' + edit('pubDate') + '",\n')
                    output.write(' title = "' + edit('title') + '",\n')
                    output.write(' book = "' + edit('bookTitle') + '",\n')
                    output.write(' pages = "' + edit('pages') + '"\n')
                    output.write(' publisher = "' + edit('publisher') + '",\n')
                    output.write(' publishedCity = "' + edit('publishedCity') + '",\n')
                    output.write('}\n')
                    output.write('\n')
        elif prompt not in options:
            pass

output.close()
