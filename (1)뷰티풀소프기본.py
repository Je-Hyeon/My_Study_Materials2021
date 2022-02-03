#http://py4e-data.dr-chuck.net/known_by_Badr.html
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
entered_count = int(input('Enter count: '))
entered_position = int(input('Enter position: '))


for i in range(entered_count):
    html = urllib.request.urlopen(url, context=ctx).read()
    print('Retrieving: ', url)
    soup = BeautifulSoup(html, 'html.parser')
    list_a = list()

    for line in soup('a'):
        list_a.append(line.get('href'))

    url = list_a[entered_position - 1]

print('last name', list_a[entered_position -1 ] )





