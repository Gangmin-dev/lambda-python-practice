import json
import pymysql

db = pymysql.connect(host = 'mytestdatabase.c1t0iaypjlcw.ap-northeast-2.rds.amazonaws.com', user = 'admin', password = '12345678', db = 'schoolexample', charset = 'utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)

def lambda_handler(event, context):
    print(event)
    body = ''
    cursor.execute('SELECT * FROM student WHERE id = {}'.format(event['queryStringParameters']['id']))
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
              <h1>%(name)s info update</h1>
                
              <form action="/student/update_process" method="post">
                    <input type="hidden" name="id" value="%(id)s">
                    <p><input type="text" name="name" placeholder="name" value="%(name)s"></p>
                    <p><input type="text" name="age" placeholder="age" value="%(age)s"></p>
                    <p>
                      <input type="submit">
                    </p>
                </form>
              <form action="/student/delete" method="post">
                <input type="hidden" name="id" value="%(id)s">
                <input type="submit" value="delete">
              </form>
            </body>
            </html>
          """ %{'name':sellected_student['name'],'age':sellected_student['age'], 'id':sellected_student['id']}
        
    
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "text/html"
        },
        'body': body
    }