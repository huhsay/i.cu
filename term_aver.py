import time
import MySQLdb as db

conn= db.connect('localhost', 'root', 'admin', 'smart')
curs=conn.cursor()
sql = "SELECT LAST_INSERT_ID(id)  FROM raw"


def aver():
	num=curs.execute(sql)
	curs.execute("select time FROM raw where id=1")
	rows=curs.fetchall()
	date=rows[0][0].date()
	stime=rows[0][0].time()

	curs.execute("select time FROM raw where id=%s",(num) )
	rows=curs.fetchall()
	etime=rows[0][0].time()
	
	curs.execute("SELECT ROUND(AVG(leftdata),1) FROM raw")
	rows=curs.fetchone()
	laver=rows[0]
	curs.execute("SELECT ROUND(AVG(rightdata),1) FROM raw")
	rows=curs.fetchone()
	raver=rows[0]
	
	print laver
	print raver

	curs.execute("INSERT INTO term(date, stime, etime, laver, raver) values (%s, %s, %s, %s, %s)", (date, stime, etime, laver, raver))
	conn.commit()
	curs.execute("truncate raw") #init table
