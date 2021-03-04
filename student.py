import json
import pymysql

db = pymysql.connect(host = 'mytestdatabase.c1t0iaypjlcw.ap-northeast-2.rds.amazonaws.com', user = 'admin', password = '12345678', db = 'schoolexample', charset = 'utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)

def lambda_handler(event, context):
    print(event)
    body = ''
    
    if('queryStringParameters' in event):
      if('id' in event['queryStringParameters']):
          cursor.execute("SELECT student.id, student.name, student.age, class.class_name, class.teacher FROM student LEFT JOIN class ON student.class_id = class.id WHERE student.id={}".format(event["queryStringParameters"]["id"]))
          sellected_student = cursor.fetchone()
          body = """
            <!doctype html>
            <html>
            <head>
              <title>%(name)s</title>
              <meta charset="utf-8">
            </head>
            <body>
              <h1><a href="/">Home</a></h1>
              <h1>%(name)s</h1>
              <a href="/student">student</a>
              <p>나이 : %(age)s </p>
              <p>반 : %(class_name)s </p>
              <p>담임선생님 : %(teacher)s </p>
              <a href="/student/update?id=%(id)s">update</a>
              <form action="/student/delete" method="post">
                <input type="hidden" name="id" value="%(id)s">
                <input type="submit" value="delete">
              </form>
            </body>
            </html>
          """ %{'name':sellected_student['name'],'age':sellected_student['age'], 'class_name':sellected_student['class_name'], 'teacher':sellected_student['teacher'], 'id':sellected_student['id']}
        
    else:
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()
        student_list = '<ul>'
        for row in students:
          print(row)
          student_list = student_list + '<li><a href="/student?id={}">{}</a></li>'.format(row['id'], row['name'])
          print(student_list)
        student_list = student_list+'</ul>'
        print(student_list)
        body = """
          <!doctype html>
          <html>
          <head>
            <title>Student list</title>
            <meta charset="utf-8">
          </head>
          <body>
            <h1><a href="/">Home</a></h1>
            <h1>Student list</h1>
            <a href="/student">student</a>
            %s
          </body>
          </html>
        """ %student_list
    print(body)
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "text/html"
        },
        'body': body
    }
