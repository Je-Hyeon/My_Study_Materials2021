# http://py4e-data.dr-chuck.net/comments_42.json
import urllib.request, urllib.parse, urllib.error
import json
import ssl


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter location: ')
data = urllib.request.urlopen(url, context=ctx).read()
real_data = json.loads(data)
count_list = list()

print('Retrieving' , url)
print('Retrieved {} characters'.format(len(real_data)))


comment_list = real_data['comments']
for i in comment_list:
    count_list.append(int(i['count']))

print('Count: ', len(count_list))
print('Sum: ', sum(count_list))



