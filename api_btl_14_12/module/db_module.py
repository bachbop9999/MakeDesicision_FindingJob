import mysql.connector


def connect_db():
    config = {
      'host': 'localhost',
      'user': 'root',
      'password': '',
      'database': 'httm_covid',
      'raise_on_warnings': True
    }

    connect = mysql.connector.connect(**config)
    return connect

def selectCovidInfor(query):
    connect = connect_db()
    cursor = connect.cursor()
    
    cursor.execute(query)
    records = cursor.fetchall()
    print("Total number of rows of data: ", cursor.rowcount)

    cursor.close()
    connect.close()
    return records