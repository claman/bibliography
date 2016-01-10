#!/usr/bin/python
import find
import regexes

output = open('output.bib', 'w')

with open('biblio.txt', 'r') as file:
    for line in file:
        author = find.getAuthor(line)
        pubDate = find.getPubDate(line)
        titleInfo = find.getTitle(line)
        title, format = titleInfo[0], titleInfo[1]

        if format == '@book':
            result = find.getBook(line, author, pubDate, title, format)
        elif format == 'excerpt':
            result = find.getExcerpt(line, author, pubDate, title)

        authorLast = author.split(',')[0].lower()
        titleFirst = title.split(' ')[0].lower()
        citekey = authorLast + pubDate + titleFirst

        print '---'
        print line + '---'
        if result['format'] == '@book':
            print 'format: ' + result['format']
            print 'author: ' + result['author']
            print 'year: ' + result['pubDate']
            print 'title: ' + result['title']
            print 'publisher: ' + result['publisher']
            print 'city: ' + result['publishedCity']
            print
        elif result['format'] == '@article':
            print 'format: ' + result['format']
            print 'author: ' + result['author']
            print 'year: ' + result['pubDate']
            print 'title: ' + result['title']
            print 'journal: ' + result['journal']
            if result['volume']:
                print 'volume: ' + result['volume']
            if result['issue']:
                print 'issue: ' + result['issue']
            print 'pages: ' + result['pages']
            print
        elif result['format'] == '@incollection':
            print 'format: ' + result['format']
            print 'author: ' + result['author']
            print 'year: ' + result['pubDate']
            print 'title: ' + result['title']
            print 'book: ' + result['bookTitle']
            print 'pages: ' + result['pages']
            print 'publisher: ' + result['publisher']
            print 'city: ' + result['publishedCity']
            print

        prompt = find.userPrompt('Add entry to bibliography? ([y]es/[s]kip/[e]dit): ')
        if prompt[1] in find.options:
            if prompt[1] in find.positive:
                if result['format'] == '@book':
                    output.write(format + '{' + citekey + ',\n')
                    output.write(' author = "' + result['author'] + '",\n')
                    output.write(' year = "' + result['pubDate'] + '",\n')
                    output.write(' title = "' + result['title'] + '",\n')
                    output.write(' publisher = "' + result['publisher'] + '",\n')
                    output.write(' publishedCity = "' + result['publishedCity'] + '",\n')
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
                elif format == '@incollection':
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
                format = find.userPrompt('Enter citation format (book, article, or incollection): ')
                if format == 'book':
                    output.write(format + '{' + find.editInfo('citekey') + ',\n')
                    output.write(' author = "' + find.editInfo('author') + '",\n')
                    output.write(' year = "' + find.editInfo('pubDate') + '",\n')
                    output.write(' title = "' + find.editInfo('title') + '",\n')
                    output.write(' publisher = "' + find.editInfo('publisher') + '",\n')
                    output.write(' publishedCity = "' + find.editInfo(
                        'publishedCity') + '",\n')
                    output.write('}\n')
                    output.write('\n')
                elif format == 'article':
                    output.write(format + '{' + find.editInfo('citekey') + ',\n')
                    output.write(' author = "' + find.editInfo('author') + '",\n')
                    output.write(' year = "' + find.editInfo('pubDate') + '",\n')
                    output.write(' title = "' + find.editInfo('title') + '",\n')
                    output.write(' journal = "' + find.editInfo('journal') + '",\n')
                    volumePrompt = str(raw_input('Specific volume (y/n): '))
                    if volumePrompt == 'y':
                        output.write(' volume = "' + find.editInfo('volume') + '",\n')
                    issuePrompt = str(raw_input('Specific issue (y/n): '))
                    if issuePrompt == 'y':
                        output.write(' issue = "' + find.editInfo('issue') + '",\n')
                    output.write(' pages = "' + find.editInfo('pages') + '"\n')
                    output.write('}\n')
                    output.write('\n')
                elif format == 'incollection':
                    output.write(format + '{' + find.editInfo('citekey') + ',\n')
                    output.write(' author = "' + find.editInfo('author') + '",\n')
                    output.write(' year = "' + find.editInfo('pubDate') + '",\n')
                    output.write(' title = "' + find.editInfo('title') + '",\n')
                    output.write(' book = "' + find.editInfo('bookTitle') + '",\n')
                    output.write(' pages = "' + find.editInfo('pages') + '"\n')
                    output.write(' publisher = "' + find.editInfo('publisher') + '",\n')
                    output.write(' publishedCity = "' + find.editInfo(
                        'publishedCity') + '",\n')
                    output.write('}\n')
                    output.write('\n')

output.close()
