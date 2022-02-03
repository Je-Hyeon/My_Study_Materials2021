import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# 여러 SQL을 실행할 때 executescript를 사용한다.
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre
''')

#설명을 넣으려고 일부러 SQL명령어를 분리했다. 이제 밑에는 여러개의 TABLE를 만든다.
#id를 신경써서 만들어야 한다. 화살표가 어디에서 어디로 가는지...

cur.executescript('''
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id INTERGER,
    len INTEGER, rating INTEGER, count INTEGER    
)
''')

fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Li.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>


#요 lookup함수는 잘 모르겠다. xml에 대한 이해가 부족한듯.
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    name = lookup(entry, 'Genre')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

#요 줄도 중요하다. 예를 들어 어떤 노래에는 genre 정보가 없을 수도 있기 때문에
# 없다면 그냥 continue해주는 것으로 코드를 짜 주어야 한다.
    if name is None or artist is None or album is None or name is None: 
        continue

    print(name, artist, album, name, count, rating, length)

# 위에서 SQL 코드를 짤 때 값들이 UNIQUE하다고 설정해 준 것이 있는데, 그것 때문에
# 만약 똑같은 이름이 두개가 있다면 무시하는 INSERT OR IGNORE으로 코드를 짜야한다.
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute(''' INSERT OR IGNORE INTO Genre (name)
        VALUES (?)''' , (name, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ?', (name,))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

#마지막으로 Track 테이블에 모든 값을 한방에 집어 넣는 코드를 짜준다.
    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ? , ? )''', 
        ( name, album_id, genre_id, length, rating, count ) )

    conn.commit()
