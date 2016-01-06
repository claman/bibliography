#!/usr/bin/python
import regexes

options = ('y',  'yep', 'yes', 'yeah', 's', 'skip', 'e', 'edit')
positive = ('y', 'yep', 'yes', 'yeah')
skipping = ('s', 'skip')
editing = ('e', 'edit')
citations = ('article', 'art', 'a', 'book', 'b', 'section', 'sec', 's')

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
    if title[0] != '"':
        return title, '@book'
    else:
        return title, 'excerpt'
def userPrompt(prompt):
    while True:
        command = str(raw_input(prompt))
        if command in options:
            return True, command
def edit(term):
    editedTerm = str(raw_input(term + ': '))
    return editedTerm
