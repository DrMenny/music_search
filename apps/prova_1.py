from ShazamAPI import Shazam

url = 'https://en.wikipedia.org/wiki/USA_björk'
author = 'Björk'

print(url)
print(author)

author = author.replace(" ", "_")

if author.lower() in url.lower():
    print('fuck yeah!')
else:
    print('none')