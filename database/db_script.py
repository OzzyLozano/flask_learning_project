import sqlite3
import bcrypt

# create connection & cursor
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# create tables
create_users_table = """
CREATE TABLE IF NOT EXISTS
  users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL UNIQUE, 
    password TEXT NOT NULL
  );
"""
cursor.execute(create_users_table)

create_posts_table = """
CREATE TABLE IF NOT EXISTS
  posts(
    post_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INT,
    title TEXT NOT NULL, 
    content TEXT NOT NULL, 
    FOREIGN KEY(user_id) REFERENCES users(user_id)
  );
"""
cursor.execute(create_posts_table)
password = 'password'
ps = 'other_password'
# add some stuff into users
cursor.execute(f"insert into users values (1, 'ozzy', '{bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')}')")
cursor.execute(f"insert into users values (2, 'admin', '{bcrypt.hashpw(ps.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')}')")

# add some stuff into posts
cursor.execute("insert into posts values (1, 1, 'title1', 'this content is from post #1')")
cursor.execute("insert into posts values (2, 1, 'title2', 'this content is from post #2')")

# show all users
cursor.execute("select * from users")
results = cursor.fetchall()
print(results)
# show all posts
cursor.execute("SELECT * FROM posts")
post_results = cursor.fetchall()
print(post_results)

# close connection
connection.commit()
connection.close()
