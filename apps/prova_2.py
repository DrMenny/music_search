from wikipedia import wikipedia

#print(wikipedia.search('Björk'))

print(wikipedia.page('Leviathan (Mastodon album)').html())

author = 'Genesis'
title = 'Broadway Melody Of 1974'

s = author + '' + title

#print(wikipedia.summary(s, ))
#wikipedia.summary(s,  sentences=99)

#def getsummary(author, title):
#    s = author + ' ' + title
#    pages = wikipedia.search(s)
#    print(pages)
#    return wikipedia.summary(pages[0])
#print(getsummary('Björk', 'Human Behavior'))

def getsummary(author, title):
    s = author + ' ' + title
    pages = wikipedia.search(s)
#    logger.debug(f'RESP: {pages}')
    return wikipedia.summary(pages[0])

#title = 'Human Behaviour'
#author = 'Björk'

#value = {"author":"Björk", "title":"Human Behavior"}

#title = value.get('title')
#author = value.get('author')

#print(getsummary(author, title))