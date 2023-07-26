import os, psycopg2, string, random,hashlib

def get_connection():
  url = os.environ['DATABASE_URL']
  connection = psycopg2.connect(url)
  return connection

def insert_user(username, password):
  sql = 'INSERT INTO auto_quiz VALUES(default, %s, %s, %s, 0)'
  salt = get_salt()
  hashed_password = get_hash(password, salt)
  try :
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (username, hashed_password, salt))
    count = cursor.rowcount
    connection.commit()
  except psycopg2.DatabaseError:
    count = 0
  finally:
    cursor.close()
    connection.close()
  return count

def get_salt():
  charset = string.ascii_letters + string.digits
  salt = ''.join(random.choices(charset, k=30))
  return salt

def get_hash(password, salt):
  b_password = bytes(password, 'utf-8')
  b_salt = bytes(salt, 'utf-8')
  hashed_password = hashlib.pbkdf2_hmac('sha256', b_password, b_salt, 1000).hex()
  return hashed_password

def authenticate(user_name, password):
  sql = 'SELECT hashed_password, salt, point FROM auto_quiz WHERE name = %s'
  flg = False
  count = None
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (user_name,))
    user = cursor.fetchone()
    if user != None:
      salt = user[1]
      hashed_password = get_hash(password, salt)
      if hashed_password == user[0]:
        flg = True
        count = user[2]
  except psycopg2.DatabaseError:
    flg = False
    count = None
  finally:
    cursor.close()
    connection.close()
  return flg, count



def get_point(name):
  sql = 'UPDATE auto_quiz SET point = point + 1 WHERE name = %s '
  try :
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (name,))
    count = cursor.rowcount
    connection.commit()
  except psycopg2.DatabaseError:
    count = 0
  finally:
    cursor.close()
    connection.close()
  return count

def getcount(username):
  sql = 'SELECT point FROM auto_quiz WHERE name = %s'
  username = username
  try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (username,))
    connection.commit()
    point = cursor.fetchone()
    point = point[0]
  finally:
    cursor.close()
    connection.close()
  return point

def ranks():
    sql = 'SELECT name, point FROM auto_quiz ORDER BY point DESC LIMIT 5;'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        rows = cursor.fetchall()  # 全ての行を取得
        rank = [row for row in rows]  # ユーザー名とポイントを含むタプルをリストに入れる
        print(rank)
    finally:
        cursor.close()
        connection.close()
    return rank
