import sqlite3  # 파이썬 기본 라이브러리

query = "악뮤"

print("검색어 :", repr(query))

connection = sqlite3.connect("melon-20230906.sqlite3")

# 모든 데이터베이스에 대해서 프로그램에서는 Cursor를 얻고
# Cursor를 통해 SELECT, UPDATE, DELETE, CREATE TABLE 등의 쿼리를 수행한다
cursor = connection.cursor()

# 실제로 실행되는 각 SQL 문에 대해 호출할 trace_callback을 등록
connection.set_trace_callback(print)

# SQL 문자열을 직접 조합하여 SQL을 실행하는 방법 -> SQL Injection 공격의 위험성이 있음
param = "%" + query + "%"
sql = f"SELECT * FROM songs WHERE 가수 LIKE '{param}' OR 곡명 LIKE '{param}'"
cursor.execute(sql)

# column_names 리스트 만들기
column_names = [desc[0] for desc in cursor.description]

song_list = cursor.fetchall()

print("list size :", len(song_list))

# 각 행을 dict 타입으로 조회하여 출력
for song_tuple in song_list:
    song_dict = dict(zip(column_names, song_tuple))
    # print(song_dict)
    # print(song_dict["곡명"], song_dict["가수"])
    print("{곡명} {가수}".format(**song_dict))

connection.close()
