
from dbm import dumb
import os
from flask import Flask, flash, render_template, redirect, url_for, request, session
from models import Database, MPengguna


app = Flask(__name__)
app.secret_key = os.urandom(12)
db = Database()
pg = MPengguna()

@app.route('/')
def index():
    data = db.read(None)

    return render_template('index.html', data = data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        pengguna = MPengguna(username, password)
        if pengguna.authenticate():
            session['username'] = username
            return redirect(url_for('indexAdmin'))
        msg = 'Username/Password yang Anda masukkan salah.'
        return render_template('login.html', msg=msg)
    return render_template('login.html')

@app.route('/admin')
def indexAdmin():
    model = Database()
    data = []
    data = model.selectDB()
    return render_template('admin.html', data=data)

@app.route('/forms/')
def forms():
    return render_template('forms.html')

@app.route('/addpemesanan', methods = ['POST', 'GET'])
def addpemesanan():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("A new data has been added")
        else:
            flash("A new data can not be added")

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/tambah/')
def tambah():
    return render_template('addPesanan.html')

@app.route('/addPesanan', methods = ['POST', 'GET'])
def addPesanan():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("A new data has been added")
        else:
            flash("A new data can not be added")

        return redirect(url_for('indexAdmin'))
    else:
        return redirect(url_for('indexAdmin'))

@app.route('/update/<int:id>/')
def update(id):
    model = Database()
    data = model.getDBbyId(id)
    return render_template('update.html', data=data)

@app.route('/updatepemesanan', methods = ['POST'])
def updatepemesanan():
    id = request.form['id']
    tanggal = request.form['tanggal']
    waktu = request.form['waktu']
    nama = request.form['nama']
    nomor_telpon = request.form['nomor_telpon']
    alamat = request.form['alamat']
    jenis_paket = request.form['jenis_paket']
    durasi = request.form['durasi']
    data = (tanggal, waktu, nama, nomor_telpon, alamat, jenis_paket, durasi, id)
    model = Database()
    model.updateDB(data)
    return redirect(url_for('indexAdmin'))

@app.route('/delete/<id>/')
def delete(id):
    model = Database()
    model.deleteDB(id)
    return redirect(url_for('indexAdmin'))



if __name__ == '__main__':
    app.run(debug=True)
