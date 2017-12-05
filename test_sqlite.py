import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor() # cursor allow us to select thing and manipulate thing

create_table = "CREATE TABLE users (id integer, username text, password text)" # this is a tuple
cursor.execute(create_table)

user_1 = (1, 'iyochan32', 'password')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query,user_1)

users = [
        (2, 'iyo', 'password'),
        (3, 'iyochan', 'password')
]

cursor.executemany(insert_query,users)

select_query = "SELECT * from users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
