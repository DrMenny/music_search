from wikipedia import wikipedia

#print(wikipedia.search('Björk'))

print(wikipedia.summary('Debut (Björk album)', sentences=10))

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