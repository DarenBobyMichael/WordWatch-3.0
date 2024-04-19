from instagrapi import Client
import json
cl = Client()

cl.login('baby_groot_smirking', 'bobymichael.123')

media_id = cl.media_id(cl.media_pk_from_url('https://www.instagram.com/p/C5691GYv1g8wdOgAn7QcUn8CiwkAhZ0dXXzLj40/'))
comment = cl.media_comments(media_id,amount=1)

for i,j in enumerate(comment[0]):
    if i==1:
        print(j[1])
