import pymysql

# open connection to the database
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='xiaoli',
                       passwd='shumaker344',
                       db='rnadb',
                       charset='utf8')
with conn:
    cur = conn.cursor()

    sql = "SELECT * FROM test"
    cur.execute(sql)
    x = cur.fetchall()
    print("="*20)
    print(x[0][0])

print("done")

