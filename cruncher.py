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

for line in file:
    author = getAuthor(line)
    pubDate = getPubDate(line)
    title = getTitle(line)

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

    prompt = str(raw_input("Add entry to bibliography? (y/n): "))
    if prompt[0] == 'y':
        if format == '@book':
            output.write(format + '{\n')
            output.write(' author: "' + author + '",\n')
            output.write(' year: "' + pubDate + '",\n')
            output.write(' title: "' + title + '",\n')
            output.write('}\n')
            output.write('\n')
        elif format == '@article':
            output.write(format + '{\n')
            output.write(' author: "' + author + '",\n')
            output.write(' year: "' + pubDate + '",\n')
            output.write(' title: "' + title + '",\n')
            output.write(' journal: "' + journal + '",\n')
            if volumeNum:
                output.write(' volume: "' + volume + '",\n')
            if issueNum:
                output.write(' issue: "' + issue + '",\n')
            output.write(' pages: "' + pages + '"\n')
            output.write('}\n')
            output.write('\n')
        elif format == '@section':
            output.write(format + '{\n')
            output.write(' author: "' + author + '",\n')
            output.write(' year: "' + pubDate + '",\n')
            output.write(' title: "' + title + '",\n')
            output.write(' book: "' + bookTitle + '",\n')
            output.write(' pages: "' + pages + '"\n')
            output.write('}\n')
            output.write('\n')

file.close()
