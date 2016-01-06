#!/usr/bin/python
import re
import find
import regexes

output = open('output.bib', 'w')

with open('biblio.txt', 'r') as file:
    for line in file:
        author = find.getAuthor(line)
        pubDate = find.getPubDate(line)
        brand = find.getTitle(line)
        title, format = brand[0], brand[1]

        if format == '@book':
            publishingInfo = regexes.publishingInfoSearch.search(line).group()
            pubExtract = regexes.publishingInfoExtract.search(
                publishingInfo).group()
            pubExtract = pubExtract.split(': ')
            publisher = pubExtract[1]
            publishedCity = pubExtract[0]
        elif format == 'excerpt':
            journalPages = regexes.journalPagesSearch.search(line)
            containingVolumeInfo = regexes.containingVolumeInfoSearch.search(
                line)
            if journalPages:
                format = '@article'
                journal = regexes.journalSearch.search(line).group()
                volumeNum = regexes.volumeSearch.search(journal)
                issueNum = regexes.issueSearch.search(journal)
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
                bookTitle = regexes.containingVolumeSearch.search(
                    bookInfo).group()
                publishingInfo = regexes.publishingInfoSearch.search(line).group()
                pubExtract = regexes.publishingInfoExtract.search(
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

        prompt = find.userPrompt('Add entry to bibliography? ([y]es/[s]kip/[e]dit): ')
        if prompt[1] in find.options:
            if prompt[1] in find.positive:
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
            elif prompt[1] in find.skipping:
                print 'Skipping\n'
                print
            elif prompt[1] in find.editing:
                format = find.userPrompt('Enter citation format (book, article, or section): ')
                if format == 'book':
                    output.write(format + '{' + edit('citekey') + ',\n')
                    output.write(' author = "' + edit('author') + '",\n')
                    output.write(' year = "' + edit('pubDate') + '",\n')
                    output.write(' title = "' + edit('title') + '",\n')
                    output.write(' publisher = "' + edit('publisher') + '",\n')
                    output.write(' publishedCity = "' + edit(
                        'publishedCity') + '",\n')
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
                    output.write(' publishedCity = "' + edit(
                        'publishedCity') + '",\n')
                    output.write('}\n')
                    output.write('\n')

output.close()
