import json
import pymysql

db = pymysql.connect(host = 'mytestdatabase.c1t0iaypjlcw.ap-northeast-2.rds.amazonaws.com', user = 'admin', password = '12345678', db = 'schoolexample', charset = 'utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)

def lambda_handler(event, context):
  body = ''
  if('queryStringParameters' in event):
    cursor.execute("SELECT * FROM student WHERE class_id = {}".format(event['queryStringParameters']['id']))
    students = cursor.fetchall()
    
    student_list = '<ul>'
    for row in students:
      # print(row)
      student_list = student_list + '<li>이름 : {}, 나이 : {}</li>'.format(row['name'], row['age'])
      # print(class_list)
    student_list = student_list+'</ul>'
    
    cursor.execute("SELECT * FROM class WHERE id = {}".format(event['queryStringParameters']['id']))
    sellected_class = cursor.fetchone()
    body = """
          <!doctype html>
          <html>
          <head>
            <title>Python Class</title>
            <meta charset="utf-8">
          </head>
          <body>
            <h1><a href="/">Home</a></h1>
            <h1>%(class_name)s</h1>
            <h2>선생님 : %(teacher)s</h2>
            %(student_list)s
            <p></p>
            <h2>학생 추가하기</h2>
              <form action="/create_student" method="post">
                <input type="hidden" name="class_id" value="%(id)s">
                <p><input type="text" name="name" placeholder="name"></p>
                <p><input type="text" name="age" placeholder="age"></p>
                <p><input type="submit" value="추가하기"></p>
              </form>
          </body>
          </html>
        """ %{'class_name':sellected_class['class_name'], 'teacher':sellected_class['teacher'], 'student_list':student_list, 'id':sellected_class['id']}
    
  else:
    cursor.execute("SELECT * FROM class")
    classes = cursor.fetchall()
    
    class_list = '<ul>'
    for row in classes:
      # print(row)
      class_list = class_list + '<li><a href="/?id={}">{}, 선생님: {}</a></li>'.format(row['id'], row['class_name'], row['teacher'])
      # print(class_list)
    class_list = class_list+'</ul>'
    # print(class_list)
    body =  """
          <!doctype html>
          <html>
          <head>
            <title>Python Class</title>
            <meta charset="utf-8">
          </head>
          <body>
            <h1><a href="/">Home</a></h1>
            <h1>Class</h1>
            <a href="/student">student</a>
            %s
          </body>
          </html>
        """ %class_list
    
  return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "text/html"
        },
        'body': body
    }
