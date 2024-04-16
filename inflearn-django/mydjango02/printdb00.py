import sqlite3  # 파이썬 기본 라이브러리

connection = sqlite3.connect("melon-20230906.sqlite3")
# 모든 데이터베이스에 대해서 프로그램에서는 Cursor를 얻고
# Cursor를 통해 SELECT, UPDATE, DELETE, CREATE TABLE 등의 쿼리를 수행한다
cursor = connection.cursor()

cursor.execute("SELECT * FROM songs")

song_list = cursor.fetchall()

# 각 행을 tuple 타입으로 조회
for song_tuple in song_list:
    print(song_tuple)

connection.close()
