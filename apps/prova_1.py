from ShazamAPI import Shazam

mp3_file_content_to_recognize = open('/home/menny/Music/Aphex Twin/Drukqs/Drukqs Disc One/01 - Jynweythek Ylow.flac', 'rb').read()

shazam = Shazam(mp3_file_content_to_recognize)
recognize_generator = shazam.recognizeSong()
res = next(recognize_generator) # current offset & shazam response to recognize requests
print(res)