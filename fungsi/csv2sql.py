from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sigempa2023'
app.config['MYSQL_DB'] = 'sistem_diseminasi'

mysql = MySQL(app)

cur = mysql.connection.cursor()
f = open('fungsi/ttm.txt', 'r')
baris = f.readlines()
f.close()
sql_insert = "INSERT INTO `tabel_ttm`(`tgl`,`tte0`,`tte1`,`tte2`,`tdr0`,`tdr1`,`tdr2`,`tbl0`,`tbl1`,`tbl2`,`lbh0`,`lbh1`,`lbh2`,`jll0`,`jll1`,`jll2`,`drb0`,`drb1`,`drb2`,`mba0`,`mba1`,`mba2`,`wda0`,`wda1`,`wda2`,`snn0`,`snn1`,`snn2`,`bbg0`,`bbg1`,`bbg2`,`sff0`,`sff1`,`sff2`) VALUES " 
data = []
for i in range(len(baris)):
    bar = baris[i].split()
    tgl = datetime.strptime(bar[0], '%d/%m/%Y')
    tgl = tgl.strftime('%Y-%m-%d')
    data = [tgl]+bar[1:]
    datanew = tuple(data)
    cur.execute(sql_insert+str(datanew))

mysql.connection.commit()

if __name__ == "__main__":
	app.run(debug=True)