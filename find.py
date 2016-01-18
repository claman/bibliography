#!/usr/bin/python
import re
import regexes

options = ('y',  'yep', 'yes', 'yeah', 's', 'skip', 'e', 'edit')
positive = ('y', 'yep', 'yes', 'yeah')
skipping = ('s', 'skip')
editing = ('e', 'edit')
citations = ('article', 'art', 'a', 'book', 'b', 'incollection', 'i', 'in', 'inc')

def getAuthor(search):
    author = regexes.authorSearch.match(search)
    author = author.group().rstrip()
    if author[len(author)-1] == ',':
        author = author[:len(author)-1]
        return author
    else:
        return author
def getPubDate(search):
    pubDate = regexes.pubDateSearch.search(search)
    pubDate = pubDate.group()
    pubDate = pubDate[:4]
    return pubDate
def getTitle(search):
    title = regexes.titleSearch.search(search)
    title = title.group()
    split = title.split('.')
    title = split[0]
    if title[0] == ' ':
        title = title[1:]
    else:
        pass
    if title[0] != '"':
        return title, '@book'
    else:
        return title, 'excerpt'
# def getPublisher(searchTerm):
#     for i in range(0, 3):
#         publisher = regexes.publishingSearch.search(searchTerm).group()
#     publisher = publisher.split(': ')
#     return (publisher[0], publisher[1])
def getBook(entry, author, pubDate, title, format):
    publishingInfo = regexes.publishingInfoSearch.search(entry).group()
    pubExtract = regexes.publishingInfoExtract.search(
        publishingInfo).group()
    pubExtract = pubExtract.split(': ')
    publisher = pubExtract[1]
    publishedCity = pubExtract[0]
    return dict([('author', author), ('pubDate', pubDate),
        ('title', title), ('format', format), ('publisher', publisher),
        ('publishedCity', publishedCity)])
def getArticle(entry, author, pubDate, title, journalPages):
    format = '@article'
    journal = regexes.journalSearch.search(entry).group()
    pages = re.search('(\d*-\d*)', journalPages.group()).group()

    volumeNum = regexes.volumeSearch.search(journal)
    issueNum = regexes.issueSearch.search(journal)

    if volumeNum or issueNum:
        journal = re.search('(\D*)(?=\s(\d|\())', journal).group()
        if volumeNum and not issueNum:
            volume = volumeNum.group()
            return dict([('author', author), ('pubDate', pubDate),
                ('title', title), ('format', format), ('journal', journal),
                ('pages', pages), ('volume', volume), ('issue', None)])
        elif issueNum and not volumeNum:
            issue = issueNum.group()
            return dict([('author', author), ('pubDate', pubDate),
                ('title', title), ('format', format), ('journal', journal),
                ('pages', pages), ('volume', None), ('issue', issue)])
        elif volumeNum and issueNum:
            volume = volumeNum.group()
            issue = issueNum.group()
            return dict([('author', author), ('pubDate', pubDate),
                ('title', title), ('format', format), ('journal', journal),
                ('pages', pages), ('volume', volume),
                ('issue', issue)])
    else:
        return dict([('author', author), ('pubDate', pubDate),
            ('title', title), ('format', format), ('journal', journal),
            ('pages', pages)])
def getInCollection(entry, containingVolumeInfo, author, pubDate, title):
    format = '@incollection'
    bookInfo = re.search('(.*\d\.)',
        containingVolumeInfo.group()).group()
    pages = re.search('(\d*-\d*)(?=\.)', bookInfo).group()
    bookTitle = regexes.containingVolumeSearch.search(
        bookInfo).group()

    publishingInfo = regexes.publishingInfoSearch.search(entry).group()
    pubExtract = regexes.publishingInfoExtract.search(
        publishingInfo).group()
    pubExtract = pubExtract.split(': ')
    publisher = pubExtract[1]
    publishedCity = pubExtract[0]

    return dict([('author', author), ('pubDate', pubDate),
        ('title', title), ('format', format), ('bookTitle', bookTitle),
        ('publisher', publisher), ('publishedCity', publishedCity),
        ('pages', pages)])
def getExcerpt(entry, author, pubDate, title):
    journalPages = regexes.journalPagesSearch.search(entry)
    containingVolumeInfo = regexes.containingVolumeInfoSearch.search(entry)
    if journalPages:
        return getArticle(entry, author, pubDate, title, journalPages)
    elif containingVolumeInfo:
        return getInCollection(entry,containingVolumeInfo, author, pubDate, title)
def userPrompt(prompt):
    while True:
        command = str(raw_input(prompt))
        if command in options:
            return True, command
def editInfo(term):
    editedTerm = str(raw_input(term + ': '))
    return editedTerm
