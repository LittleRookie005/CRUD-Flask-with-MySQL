from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'data_mahasiswa'
mysql = MySQL(app)

@app.route('/')
def index():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM mahasiswa")
	data = cur.fetchall()
	cur.close()
	return render_template('index.html', mahasiswas=data)

@app.route('/simpan',methods=["GET", "POST"])
def simpan():
	details = request.form
	NIM = details['nim']
	Nama = details['nama']
	Alamat = details['alamat']
	Program_Studi = details['prodi']
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO mahasiswa (nim, nama, alamat, prodi) VALUE (%s, %s, %s, %s)",(NIM, Nama, Alamat, Program_Studi))
	mysql.connection.commit()
	return redirect(url_for('index'))

@app.route('/update',methods=["GET", "POST"])
def update():
	details = request.form
	no = details['no']
	NIM = details['nim']
	Nama = details['nama']
	Alamat = details['alamat']
	Program_Studi = details['prodi']
	cur = mysql.connection.cursor()
	cur.execute("UPDATE mahasiswa SET nim=%s, nama=%s, alamat=%s, prodi=%s WHERE no=%s", (NIM, Nama, Alamat, Program_Studi, no))
	mysql.connection.commit()
	return redirect(url_for('index'))

@app.route('/hapus/<string:no>')
def hapus(no):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM mahasiswa WHERE no=%s", (no))
	mysql.connection.commit()
	return redirect(url_for('index'))

@app.route('/search', methods=["POST"])
def search():
	cur = mysql.connection.cursor()
	keyword = request.form['search']
	cur.execute("SELECT * FROM mahasiswa WHERE nama LIKE  '%{}%' ".format(keyword))
	data = cur.fetchall()
	return render_template('search.html', data=data)

if __name__ == '__main__':
	app.run(debug=True)
