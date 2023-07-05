import config
import pymysql

class Database:
    def connect(self):
        return pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='bersihin')

    def __init__ (self, id=None, tanggal=None, waktu=None, nama=None, nomor_telpon=None, alamat=None, jenis_paket=None, durasi=None):
        self.id = id
        self.tanggal = tanggal
        self.waktu = waktu
        self.nama = nama
        self.nomor_telpon = nomor_telpon
        self.alamat = alamat
        self.jenis_paket = jenis_paket
        self.durasi = durasi

    def openDB(self):
        global db, cursor
        db = pymysql.connect(
            host = config.DB_HOST,
            user = config.DB_USER,
            password = config.DB_PASSWORD,
            database = config.DB_NAME)
        cursor = db.cursor()

    def closeDB(self):
        global db, cursor
        db.close()
    
    def selectDB(self):
        self.openDB()
        cursor.execute("SELECT * FROM pemesanan")
        container = []
        for id, tanggal, waktu, nama, nomor_telpon, alamat, jenis_paket, durasi in cursor.fetchall():
            container.append((id, tanggal, waktu, nama, nomor_telpon, alamat, jenis_paket, durasi))
        self.closeDB()
        return container

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM pemesanan order by name asc")
            else:
                cursor.execute("SELECT * FROM pemesanan where id = %s order by name asc", (id))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self,data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO pemesanan(tanggal,waktu,nama,nomor_telpon,alamat,jenis_paket,durasi) VALUES(%s, %s, %s, %s, %s, %s, %s)", (data['tanggal'],data['waktu'],data['nama'],data['nomor_telpon'],data['alamat'],data['jenis_paket'],data['durasi']))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def getDBbyId(self, id):
        self.openDB()
        cursor.execute("select * from pemesanan where id='%s'" % id)
        data = cursor.fetchone()
        return data

    

    def updateDB(self, data):
        self.openDB()
        cursor.execute("update pemesanan set tanggal='%s', waktu='%s', nama='%s', nomor_telpon='%s', alamat='%s', jenis_paket='%s', durasi='%s' where id=%s" % data)
        db.commit()
        self.closeDB

    
    def deleteDB (self, id):
        self.openDB()
        cursor.execute("delete from pemesanan where id=%s" % id )
        db.commit()
        self.closeDB() 

    
class MPengguna():
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def openDB(self):
        global db, cursor
        db = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        cursor = db.cursor()
    
    def selectDB(self, username):
        self.username = username
        self.openDB()
        cursor.execute("SELECT * FROM tb_users WHERE username = '%s'" % self.username)
        container = cursor.fetchall()
        self.closeDB
        return container

    def closeDB(self):
        global db, cursor
        db.close()
    
    def authenticate(self):
        self.openDB()
        cursor.execute("SELECT COUNT(*) FROM tb_users WHERE username = '%s' AND password = '%s'" %(self.username, self.password))
        count_account = (cursor.fetchone())[0]
        self.closeDB()
        return True if count_account>0 else False