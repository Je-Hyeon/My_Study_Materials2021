# http://py4e-data.dr-chuck.net/comments_42.xml
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

Enter_location = input('Enter location: ')
print('Retrieving ', Enter_location)

data = urllib.request.urlopen(Enter_location, context=ctx).read()
tree = ET.fromstring(data) #나무를 만들었다. 여기가 핵심.

counts = tree.findall('.//count')   #데이터를 어떻게 추출하는 지도 중요한데 그건 파란색 노트에 정리해 뒀음.
real_list = []
count_of_count = 0

for i in counts:
    real_list.append(int(i.text))
    count_of_count = count_of_count + 1

print('Retrieved {} characters'.format(len(data.strip())))
print('Count: ', count_of_count)
print('Sum: ', sum(real_list))



