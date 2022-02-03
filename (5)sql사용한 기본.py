import sqlite3
import re

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

#테이블 이름은 카운트, org와 count 두가지 열이 있음
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname,'r')

for line in fh:
    if line.startswith('From: '):
        all_org = re.findall('@(.+\s)' ,line)  # findall은 리스트를 반환 함.(모든 주소로 구성됨)
        
        for org in all_org:                    #따라서 반복문을 한번 더 돌린다. 

            cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ) )
            row = cur.fetchone()
            if row is None:
                cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
            else:
                cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))

conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()    
 