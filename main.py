import requests # http requests

from bs4 import BeautifulSoup # used for web scrapping

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

now = datetime.datetime.now()

# email content place holder
content = ''

# actualling extracting the data
def extract_news(url):
    print('Extracting Hacker news story.....')
    cnt = ''
    cnt +=('<b>HN Top Stories<b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

                # used enumerate because we need numbers(1,2,...) in the email part
    for i, tag in enumerate(soup.find_all('td', attrs= {'class':'title', 'valign':''})): # this stated that should be extracted from website
        cnt += ((str(i+1)+' :: '+tag.text+"\n"+'<br>') if tag.text != 'More' else '')
                # (1 :: this is the text inside the text tag <br> )
    return cnt
cnt = extract_news('http://news.ycombinator.com/')
content +=cnt
content += ('<br>--------------------<br>')
content += ('<br><br>End of Message')


# sending the email

print('Composing the Email')

SERVER = 'smtp.gmail.com'# thesmtp server
PORT = 587
FROM = 'tarankalirao1@gmail.com'
TO =   'kalitara2002@gmail.com'
PASS = '---'

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ''+str(now.day)+'-'+str(now.month)+'-'+str(now.year)

msg.attach(MIMEText(content, 'html'))

print('Initialing Server')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)# set it as 1 if we wanna see the messages
server.ehlo()# initialite communication
server.starttls()
server.login(FROM, PASS)
server.send_message(FROM, TO, msg.as_string())

print('Email sent')

server.quit()