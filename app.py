from flask import Flask, jsonify, redirect, request, url_for, render_template
from markupsafe import escape
import sqlite3
import bcrypt

app = Flask(__name__)

# path for db connection
db_path = './database/database.db'

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/test')
def test():
  return render_template('test-form.html')

@app.route('/login', strict_slashes=False)
def login():
  return render_template('login.html')

@app.route('/profile/<id>')
def profile(id):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute(f"select username from users where username='{id}';")
  user_data = cursor.fetchone()
  connection.commit()
  connection.close()
  if user_data:
    return render_template('profile.html', id=id)
  else:
    return render_template('404.html')

@app.route('/handle_login', methods=['GET', 'POST'])
def handle_login():
  # set up connection & cursor to get users and passwords
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  username = request.args['id']
  password = request.args['password']
  cursor.execute(f"select username, password from users where username='{username}';")
  user_data = cursor.fetchone()
  connection.commit()
  connection.close()
  if (request.method == 'GET'):
    if user_data:
      if bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
        return redirect(url_for('profile', id=username))
      else:
        return f'<h1>Invalid password</h1>'
    else:
      return f'<h1>Invalid username.</h1>'
  else: return '<h1>Error: Not a GET request.</h1>'

@app.route('/register', strict_slashes=False)
def register():
  return render_template('register.html')

@app.route('/handle_registry', methods=['GET', 'POST'])
def handle_registry():
  # set up connection & cursor to get users and passwords
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  username = request.form['id']
  password = request.form['password']
  cursor.execute(f"select username from users where username='{username}';")
  user_data = cursor.fetchone()
  if (request.method == 'POST'):
    if user_data:
      return '<h1>Already Registered</h1>'
    else:
      hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
      print(username, hashed_password)
      cursor.execute(f"insert into users(username, password) values (?, ?)", (username, hashed_password))
      connection.commit()
      connection.close()
      return redirect(url_for('login'))
  else: return '<h1>Error: Not a POST request.</h1>'

@app.route('/getUsers')
def get_users():
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  users = cursor.execute(f"select user_id, username, password from users;").fetchall()
  connection.commit()
  connection.close()
  user_list = [{"id": user[0], "username": user[1], "password": user[2]} for user in users]
  return jsonify(user_list)

@app.route('/app_login', methods=['POST'])
def app_login():
  data = request.get_json()
  user_id = data.get("user_id")
  password = data.get("password")
  print(f"Received login attempt for user_id: {user_id}")
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute(f"select user_id, username, password from users where user_id={user_id};")
  user = cursor.fetchone()
  connection.close()
  if not user:
    print('user not found')
    return jsonify({"message": 'User not found'}), 404
  elif bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
    print(f"User {user_id} logged in successfully")
    return jsonify({"id": user[0], "username": user[1], "password": user[2]}), 200
  else:
    print('wrong password')
    return jsonify({"message": "Wrong password"}), 401

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

# @app.route('/post/<int:post_id>')
# def showPost(post_id):
#   return f'This is a post with id: {escape(post_id)}'

# with app.test_request_context():
#   print(url_for('index'))
