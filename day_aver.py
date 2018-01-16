import MySQLdb as db
import time
import datetime
from datetime import timedelta, date


def day_aver():
	conn=db.connect('localhost', 'root', 'admin', 'smart')
	curs=conn.cursor()
	d=timedelta(days=-1)
	t=date.today()
	y=t+d
	sql="SELECT AVG(laver), AVG(raver) FROM term  where date=%s"
	curs.execute(sql,(y))  
	rows=curs.fetchall()
	if not rows:
		sql2= "INSERT INTO day(date, laver, raver) VALUES(%s, %s, %s)"
		curs.execute(sql2,(y,rows[0][0],rows[0][1]))
		conn.commit()

day_aver()
