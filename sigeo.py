from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from flask_mysqldb import MySQL
from calendar import monthrange
from datetime import datetime, timedelta
from dateutil import tz
import openpyxl
import time
import subprocess,os
import bcrypt
from zipfile import ZipFile
from fungsi.dataproc import *
from werkzeug.utils import secure_filename
import telebot
from lockfile import LockFile

#os.system('whoami')


app = Flask(__name__)
app.secret_key = "membuatLOginFlask1"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sigempa2023'
app.config['MYSQL_DB'] = 'sistem_diseminasi'
app.config["UPLOAD_FOLDER"] = "static/upload/"

mysql = MySQL(app)

@app.route('/htmltes')
def tes():
    
    return render_template('htmltes.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login(): 

    if request.method == 'POST':
        usr = request.form['username']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM users WHERE user=%s",(usr,))
        user = curl.fetchone()
        print('ini user',user)
        #print(user['password'])
        curl.close()

        if user is not None and len(user) > 0 :
            print('ini user1',user[2].encode('utf-8'))
            if bcrypt.hashpw(password, user[2].encode('utf-8')) == user[2].encode('utf-8'):
                session['id'] = user[0]
                session['user'] = user[1]
                return redirect(url_for('tambahberita'))
            
            else :
                #session.clear()
                flash("Wrong Password !!")
                return render_template("loginpage.html")
                #return redirect(url_for('login'))
        elif usr == "user": 
            pwd = '$2b$12$H6wqyGBFkBaZOuMVVwwk4Oy.OFqhPswKK3zlbra5VcDXhYH7VhymO'
            if bcrypt.hashpw(password, pwd.encode('utf-8')) == pwd.encode('utf-8'):
                session['user_stakeholder'] = usr
                return redirect(url_for('stakeholder'))
            
            else :
                #session.clear()
                flash("Wrong Password !!")
                return render_template("loginpage.html")
                #return redirect(url_for('login'))
        else :
            flash("User Not Found !!")
            return render_template("loginpage.html")
    else:
        #session.clear()
        return render_template("loginpage.html")
    
    #return render_template("loginpage.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login')) 

@app.route('/petirpgr')
def petirpgr():
    if 'user' in session:
        

        return render_template('petir_pgr.html')
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

@app.route('/hapus/<string:id_data>', methods=["GET"])
def hapus(id_data):
    if 'user' in session:
        cur = mysql.connection.cursor()
        sql = f"DELETE FROM `berita` WHERE `id`='{id_data}'"
        a = cur.execute(sql)
        mysql.connection.commit()
        return redirect(request.referrer)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    
@app.route('/berita/<string:slug>', methods=["GET"])
def berita_detail(slug):
        print(slug)
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `berita` WHERE `slug`='{slug}'")
        berita = cur.fetchall()
        berita = berita[0]
        isi = berita[4]
        par1 = isi.split('%')[0]
        par2 = isi.split('%')[1]
        isipar = [par1,par2]

        sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 10"
        cur.execute(sql)
        tabel = cur.fetchall()
        return render_template('berita.html',isiberita=isipar, berita=berita,listberita=tabel)


@app.route('/tambahberita')
def tambahberita():
    if 'user' in session:
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 10"
        cur.execute(sql)
        tabel = cur.fetchall()
        print(tabel)


        return render_template('tambahberita.html', data=tabel)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    
@app.route('/permintaandatanolrupiah')
def pelayanannolrupiah():
    
    return render_template('pelayanannolrupiah.html')

@app.route('/profil')
def profil():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 10"
    cur.execute(sql)
    tabel = cur.fetchall()
    berita = tabel[0]
    return render_template('profil.html', berita=berita,listberita=tabel)

@app.route('/sejarah')
def sejarah():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 10"
    cur.execute(sql)
    tabel = cur.fetchall()
    berita = tabel[0]
    return render_template('sejarah.html', berita=berita,listberita=tabel)

@app.route('/tupoksi')
def tupoksi():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 10"
    cur.execute(sql)
    tabel = cur.fetchall()
    berita = tabel[0]
    return render_template('tupoksi.html', berita=berita,listberita=tabel)

@app.route('/visidanmisi')
def visimisi():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 10"
    cur.execute(sql)
    tabel = cur.fetchall()
    berita = tabel[0]
    return render_template('visimisi.html', berita=berita,listberita=tabel)

@app.route('/kontakkami')
def kontak():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 10"
    cur.execute(sql)
    tabel = cur.fetchall()
    berita = tabel[0]
    return render_template('kontak.html', berita=berita,listberita=tabel)

@app.route('/kirimpesan',methods=['POST'])
def pesan():
    nama = request.form['name']
    nohp = request.form['nohp']
    judul = request.form['subject']
    isi = request.form['message']

    ID_TELE = -908862499
    api_key = '6586312439:AAGoFWf9TPBS_YQOQvUlDn84aJnQLsVOcU0' #API Bot
    bot = telebot.TeleBot(api_key)

    pesan = (u"\U000026A0"+"*ADA PESAN DARI WEBSITE*\nNama: "+nama+"\nNo.Wa: "+nohp+"\nJudul: "+judul+"\nIsi Pesan: "+isi)
    bot.send_message(ID_TELE, pesan,parse_mode='Markdown')

    # return bot.send_message(ID_TELE, pesan,parse_mode='Markdown')
    # flash("","sukses")
    return "OK"



@app.route('/permintaandata')
def pelayanan():
    
    return render_template('pelayanan.html')


@app.route('/pelayanan/<string:tipe>',methods=['GET', 'POST'])

def pelayanansubmit(tipe):
    if request.method == 'GET':
        tipe = tipe
    else:
        nama = request.form['nama']
        alamat = request.form['alamat']
        ptn = request.form['ptn']
        jenis_data = request.form['jenis_data']
        nohp = request.form['nohp']
        email = request.form['email']
        berkas = request.files['berkas']
        namabrks = secure_filename(berkas.filename)

        tgl = datetime.now().strftime("%y%m%d%H%M%S")
        fsave = 'pelayanan/'+str(nama.split()[0])+tgl+'_'+namabrks
        berkas.save(app.config['UPLOAD_FOLDER'] + fsave)

        # ID_TELE = 136845733 #ID Telegram Stageof
        ID_TELE = -837283966
        api_key = '6586312439:AAGoFWf9TPBS_YQOQvUlDn84aJnQLsVOcU0' #API Bot 

        bot = telebot.TeleBot(api_key)
        if tipe == 'nolrupiah':
            jenislayanan = "*PERMINTAAN DATA TARIF NOL RUPIAH*"
        else:
            jenislayanan = "*PERMINTAAN DATA BERTARIF*"
            
        pesan = (jenislayanan+"\nNama: "+nama+"\nAlamat: "+alamat+"\nInstansi/Perguruan Tinggi: "+ptn+
                "\nJenis Data: "+jenis_data+"\nNo.Hp (WA): "+nohp+"\nEmai: "+email)
        bot.send_message(ID_TELE, pesan,parse_mode='Markdown')

        file = open('static/upload/'+fsave,'rb')
        bot.send_document(ID_TELE, file)

        print(nama,alamat,ptn,jenis_data,nohp,email,berkas)
        # return render_template('pelayanannolrupiah.html')
        if tipe == 'nolrupiah':
            flash("","sukses")
            return redirect(url_for('pelayanannolrupiah'))
        else:
            flash("","sukses")
            return redirect(url_for('pelayanan'))

    
@app.route('/hilal')
def hilal():
    if 'user' in session:
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM `hilal` ORDER BY `id` DESC LIMIT 10"
        cur.execute(sql)
        tabel = cur.fetchall()
        print(tabel)


        return render_template('tambahdatahilal.html', data=tabel)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    
    
    
@app.route('/hilal/submit',methods=["POST"])
def submithilal():
    if 'user' in session:
        bulan_hij = request.form['bulan_hij']
        tahun_hij = request.form['tahun_hij']
        t_obs = request.form['t_obs']
        t_konj = request.form['t_konj']
        ttm_matahari = request.form['ttm_matahari']
        ttm_bulan = request.form['ttm_bulan']
        az_matahari = request.form['az_matahari']
        az_bulan = request.form['az_bulan']
        tinggi_hilal = request.form['tinggi_hilal']
        elongasi = request.form['elongasi']
        umur_bulan = request.form['umur_bulan']
        lag = request.form['lag']
        fi_bulan = request.form['fi_bulan']

        # print(judul,tanggal,penulis,slug,namagbr,isi)

        insert = (bulan_hij,tahun_hij,t_obs,t_konj,ttm_matahari,ttm_bulan,az_matahari,az_bulan,tinggi_hilal,elongasi,umur_bulan,lag,fi_bulan)
        sql_insert = ("INSERT INTO `hilal`(`bulan_hij`,`tahun_hij`,`t_obs`,`t_konj`,`ttm_matahari`,`ttm_bulan`,`az_matahari`,`az_bulan`,`tinggi_hilal`,`elongasi`,`umur_bulan`,`lag`,`fi_bulan`) VALUES " + str(insert))
        cur = mysql.connection.cursor()
        cur.execute(sql_insert)
        mysql.connection.commit()

        # cur = mysql.connection.cursor()
        # sql = "SELECT * FROM `berita` ORDER BY `id` DESC LIMIT 10"
        # cur.execute(sql)
        # tabel = cur.fetchall()
        # print(tabel)
        return redirect(url_for('hilal'))
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    
@app.route('/hapushilal/<string:id_data>', methods=["GET"])
def hapushilal(id_data):
    if 'user' in session:
        cur = mysql.connection.cursor()
        sql = f"DELETE FROM `hilal` WHERE `id`='{id_data}'"
        a = cur.execute(sql)
        mysql.connection.commit()
        return redirect(request.referrer)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

    
@app.route('/tambahberita/submit',methods=["POST"])
def submit():
    if 'user' in session:
        judul = request.form['judul']
        tanggal = request.form['tanggal']
        penulis = request.form['penulis']
        gambar = request.files['gambar']
        isi1 = request.form['isi1']
        isi2 = request.form['isi2']
        slug = judul.replace(' ', '-')
        slug = slug.replace('.', '%')
        slug = slug.replace(',', '%')
        slug = slug.replace('/', '%')
        isi = isi1+'%'+isi2
        namagbr = secure_filename(gambar.filename)
        gambar.save(app.config['UPLOAD_FOLDER'] + namagbr)

        # print(judul,tanggal,penulis,slug,namagbr,isi)

        insert = (tanggal,judul,slug,isi,penulis,namagbr)
        sql_insert = ("INSERT INTO `berita`(`tanggal`,`judul`,"
                    "`slug`,`isi`,`penulis`,`gambar`) VALUES " + str(insert))
        cur = mysql.connection.cursor()
        cur.execute(sql_insert)
        mysql.connection.commit()

        # cur = mysql.connection.cursor()
        # sql = "SELECT * FROM `berita` ORDER BY `id` DESC LIMIT 10"
        # cur.execute(sql)
        # tabel = cur.fetchall()
        # print(tabel)
        return redirect(url_for('tambahberita'))
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))
    



@app.route('/')
def index():
    hari = 90
    tdy = datetime.today()
    end = (tdy - timedelta(days=1))
    start = (tdy - timedelta(days=hari))
    yest = end
    hari=((end-start).days)+1
    seminggu = start.strftime('%Y-%m-%d')
    cur = mysql.connection.cursor()
    sql_filter = "SELECT * FROM db_gempa WHERE `Origin Date` BETWEEN %s AND %s ORDER BY `Origin Date` ASC, `Origin Time` ASC"
    condition = (seminggu, yest)
    cur.execute(sql_filter, condition)
    par = cur.fetchall()

    sql_last = "SELECT * FROM db_gempa ORDER BY `Origin Date` DESC, `Origin Time` DESC LIMIT 1"
    cur.execute(sql_last)
    last = cur.fetchall()

    var = last[0][0]
    param = infogempa(var)


    # petir
    hari = 14
    tdy = datetime.today()
    end = (tdy - timedelta(days=1))
    start = (tdy - timedelta(days=hari))


    f = open('fungsi/coord.cfg', 'r')
    baris = f.readlines()
    f.close()
    coord = baris[0].split(' ')
    batas = [coord[0],coord[1],coord[2],coord[3]]

    databases = fromdbsta(start,end)
    fileout = 'fungsi/sambaran.dat'
    readdb3(databases,fileout,batas)

    fcgp = open('fungsi/sambarancgp.dat', 'r')
    fcgm = open('fungsi/sambarancgm.dat', 'r')
    fic = open('fungsi/sambaranic.dat', 'r')
    samcgp,samcgm,samic=[],[],[]
    baris = fcgp.readlines()
    for i in range(len(baris)):
        bar = baris[i].split()
        samcgp+=[[bar[0],bar[1]]]
    baris = fcgm.readlines()
    for i in range(len(baris)):
        bar = baris[i].split()
        samcgm+=[[bar[0],bar[1]]]
    baris = fic.readlines()
    for i in range(len(baris)):
        bar = baris[i].split()
        samic+=[[bar[0],bar[1]]]
    
    datasam = fileout
    f = open(datasam, 'r')
    sam = []
    baris = f.readlines()
    for i in range(len(baris)):
        bar = baris[i].split()
        sam+=[[bar[0],bar[1],float(bar[4])]]

    total = [len(sam),len(samcgp),len(samcgm),len(samic)]

    cur = mysql.connection.cursor()
    sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 3"
    cur.execute(sql)
    tabel = cur.fetchall()
    berita1 = tabel[0][0]
    # print(tabel[0][0])


    # TERBIT TERBENAM 
    now = datetime.now()
    besok = (now + timedelta(days=1))
    besok = besok.strftime('%Y-%m-%d')
    sql = f"SELECT `tte0`,`tte1`,`tdr0`,`tdr1`,`tbl0`,`tbl1`,`lbh0`,`lbh1`,`jll0`,`jll1`,`drb0`,`drb1`,`mba0`,`mba1`,`wda0`,`wda1`,`snn0`,`snn1`,`bbg0`,`bbg1`,`sff0`,`sff1` FROM tabel_ttm WHERE `tgl`='{besok}'"
    cur.execute(sql)
    ttm = cur.fetchall()
    ttm = ttm[0]
    i=0
    terbit = []
    terbenam = []
    kota = ['Ternate','Tidore','Tobelo','Labuha','Jailolo','Daruba','Maba','Weda','Sanana','Bobong','Sofifi']
    while i < len(ttm):
        if i == 0 or (i % 2) == 0:
            rise = datetime.strptime(str(ttm[i]),"%H:%M:%S")
            trbt = rise.strftime("%H:%M")
            terbit += [trbt]
        else:
            set = datetime.strptime(str(ttm[i]),"%H:%M:%S")
            trbnm = set.strftime("%H:%M")
            terbenam += [trbnm]
        i += 1

    ttm = []
    for i in range(len(kota)):
        ttm += [[kota[i],terbit[i],terbenam[i]]]


    # HILAL
    now = now.replace(hour=0,minute=0,second=0,microsecond=0)
    d30 = (now + timedelta(days=30))
    sql_filter = "SELECT * FROM `hilal` WHERE `t_obs` BETWEEN %s AND %s ORDER BY `t_obs` ASC"
    condition = (now,d30)
    cur.execute(sql_filter, condition)
    hilal = cur.fetchall()
    datahilal = hilal[0]
    print(datahilal)
    azsun = datahilal[7]
    azmoon = datahilal[8]
    if float(azmoon) < float(azsun):
        pos = 'Selatan'
    else:
        pos = 'Utara'
    
    posisi = 'Bulan di Sebelah '+pos+' - Atas Matahari'


    tobs = datahilal[3]
    tobs = tobs.strftime("%Y-%m-%d")
    tkonj = datahilal[4]
    sunset = datahilal[5]
    moonset = datahilal[6]
    tinggi = datahilal[9]
    bulan = datahilal[1]+' '+datahilal[2]+' H'

    hilal = [tobs,tkonj,sunset,moonset,tinggi,posisi,bulan]

    vis = visitcount()

    if float(vis) > 1000:
        visitor = ('%.1f') % (float(vis)/1000)
        visitor = visitor+'k'
    else:
        visitor = str(vis)

    
    return render_template('index_new.html',vis=visitor,hilal=hilal, ttm=ttm,berita=[tabel,berita1],data=par,lasteq=last,infogempa=param, total=total,sam=sam)

def infogempa(var):
    cur = mysql.connection.cursor()

    id = var
    cur = mysql.connection.cursor()
    sql = f"SELECT * FROM db_gempa WHERE `Event ID`='{id}'"
    param = cur.execute(sql)
    par = cur.fetchall()
    par = par[0]
    date,time,lat,long,depth,mag,ket,info = par[1],par[2],par[3],par[4],par[5],par[6],par[7],par[8]
    date = date.strftime('%Y-%m-%d')
    #time = time.strftime('%H:%M:%S')

    print(date)
    
    timeutc = date + ' ' + str(time)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(timeutc[0:19], '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    ot = utc.astimezone(to_zone)
    tgl = ot.strftime("%d")
    bulan = ot.strftime("%b")
    tahun = ot.strftime("%y")
    waktu = ot.strftime("%X")
    bujur = ('%.2f') % float(long)
    depth = ('%.0f') % float(depth)
    if float(lat) > 0:
        NS = "LU"
        ltg = ('%.2f') % float(lat)
    else:
        NS = "LS"
        ltg = ('%.2f') % abs(float(lat))
    mag = ('%.1f') % float(mag)
    keterangan = ket.split()
    min_jarak = keterangan[0]
    arah = keterangan[2]
    minkota = keterangan[3]

    if len(info) > 3:
        param = ('Info Gempa Mag:' + mag + ', ' + tgl + '-' + bulan + '-' + tahun + ' ' + waktu +
                ' WIT, Lok: ' + ltg + ' ' + NS + ', ' + bujur + ' BT (' + min_jarak + ' km ' +
                arah +' '+ minkota + '), Kedlmn:' + depth + ' Km, '+info+' ::BMKG-TNT')
    else:
        param = ('Info Gempa Mag:' + mag + ', ' + tgl + '-' + bulan + '-' + tahun + ' ' + waktu +
                ' WIT, Lok: ' + ltg + ' ' + NS + ', ' + bujur + ' BT (' + min_jarak + ' km ' +
                arah +' '+ minkota + '), Kedlmn:' + depth + ' Km ::BMKG-TNT')
    return param


@app.route('/stakeholder')
def stakeholder():
    if 'user_stakeholder' in session or 'user' in session:
        hari = 90
        tdy = datetime.today()
        end = (tdy - timedelta(days=1))
        start = (tdy - timedelta(days=hari))
        yest = end
        hari=((end-start).days)+1
        seminggu = start.strftime('%Y-%m-%d')
        cur = mysql.connection.cursor()
        sql_filter = "SELECT * FROM db_gempa WHERE `Origin Date` BETWEEN %s AND %s ORDER BY `Origin Date` ASC, `Origin Time` ASC"
        condition = (seminggu, yest)
        cur.execute(sql_filter, condition)
        par = cur.fetchall()

        sql_last = "SELECT * FROM db_gempa ORDER BY `Origin Date` DESC, `Origin Time` DESC LIMIT 1"
        cur.execute(sql_last)
        last = cur.fetchall()

        var = last[0][0]
        param = infogempa(var)


        # petir
        hari = 14
        tdy = datetime.today()
        end = (tdy - timedelta(days=1))
        start = (tdy - timedelta(days=hari))


        f = open('fungsi/coord.cfg', 'r')
        baris = f.readlines()
        f.close()
        coord = baris[0].split(' ')
        batas = [coord[0],coord[1],coord[2],coord[3]]

        databases = fromdbsta(start,end)
        fileout = 'fungsi/sambaran.dat'
        readdb3(databases,fileout,batas)

        fcgp = open('fungsi/sambarancgp.dat', 'r')
        fcgm = open('fungsi/sambarancgm.dat', 'r')
        fic = open('fungsi/sambaranic.dat', 'r')
        samcgp,samcgm,samic=[],[],[]
        baris = fcgp.readlines()
        for i in range(len(baris)):
            bar = baris[i].split()
            samcgp+=[[bar[0],bar[1]]]
        baris = fcgm.readlines()
        for i in range(len(baris)):
            bar = baris[i].split()
            samcgm+=[[bar[0],bar[1]]]
        baris = fic.readlines()
        for i in range(len(baris)):
            bar = baris[i].split()
            samic+=[[bar[0],bar[1]]]
        
        datasam = fileout
        f = open(datasam, 'r')
        sam = []
        baris = f.readlines()
        for i in range(len(baris)):
            bar = baris[i].split()
            sam+=[[bar[0],bar[1],float(bar[4])]]

        total = [len(sam),len(samcgp),len(samcgm),len(samic)]

        cur = mysql.connection.cursor()
        sql = "SELECT * FROM `berita` ORDER BY `tanggal` DESC LIMIT 3"
        cur.execute(sql)
        tabel = cur.fetchall()
        berita1 = tabel[0][0]
        print(tabel[0][0])


        # TERBIT TERBENAM 
        now = datetime.now()
        besok = (now + timedelta(days=1))
        besok = besok.strftime('%Y-%m-%d')
        sql = f"SELECT `tte0`,`tte1`,`tdr0`,`tdr1`,`tbl0`,`tbl1`,`lbh0`,`lbh1`,`jll0`,`jll1`,`drb0`,`drb1`,`mba0`,`mba1`,`wda0`,`wda1`,`snn0`,`snn1`,`bbg0`,`bbg1`,`sff0`,`sff1` FROM tabel_ttm WHERE `tgl`='{besok}'"
        cur.execute(sql)
        ttm = cur.fetchall()
        ttm = ttm[0]
        i=0
        terbit = []
        terbenam = []
        kota = ['Ternate','Tidore','Tobelo','Labuha','Jailolo','Daruba','Maba','Weda','Sanana','Bobong','Sofifi']
        while i < len(ttm):
            if i == 0 or (i % 2) == 0:
                rise = datetime.strptime(str(ttm[i]),"%H:%M:%S")
                trbt = rise.strftime("%H:%M")
                terbit += [trbt]
            else:
                set = datetime.strptime(str(ttm[i]),"%H:%M:%S")
                trbnm = set.strftime("%H:%M")
                terbenam += [trbnm]
            i += 1

        ttm = []
        for i in range(len(kota)):
            ttm += [[kota[i],terbit[i],terbenam[i]]]


        # HILAL
        now = now.replace(hour=0,minute=0,second=0,microsecond=0)
        d30 = (now + timedelta(days=30))
        sql_filter = "SELECT * FROM `hilal` WHERE `t_obs` BETWEEN %s AND %s ORDER BY `t_obs` ASC"
        condition = (now,d30)
        cur.execute(sql_filter, condition)
        hilal = cur.fetchall()
        datahilal = hilal[0]
        print(datahilal)
        azsun = datahilal[7]
        azmoon = datahilal[8]
        if float(azmoon) < float(azsun):
            pos = 'Selatan'
        else:
            pos = 'Utara'
        
        posisi = 'Bulan di Sebelah '+pos+' - Atas Matahari'


        tobs = datahilal[3]
        tobs = tobs.strftime("%Y-%m-%d")
        tkonj = datahilal[4]
        sunset = datahilal[5]
        moonset = datahilal[6]
        tinggi = datahilal[9]
        bulan = datahilal[1]+' '+datahilal[2]+' H'

        hilal = [tobs,tkonj,sunset,moonset,tinggi,posisi,bulan]
        vis = visitcount()

        if float(vis) > 1000:
            visitor = ('%.1f') % (float(vis)/1000)
            visitor = visitor+'k'
        else:
            visitor = str(vis)

        # print("ini adalah visitcount",visitor)

        
        
        return render_template('index_stakeholder.html',vis=visitor,hilal=hilal, ttm=ttm,berita=[tabel,berita1],data=par,lasteq=last,infogempa=param, total=total,sam=sam)
    else:
        flash("Please, Login First !!")
        return redirect(url_for('login'))

def visitcount():
	lock = LockFile("fungsi/visitors.txt")
	with lock:
		with open("fungsi/visitors.txt", "r+") as f:
			fileContent = f.read()

			if fileContent == "":
				count = 1
			else:
				count = int(fileContent) + 1
			
			f.seek(0)
			f.write(str(count))
			f.truncate()
			
			return str(count)

def infogempa(var):
    cur = mysql.connection.cursor()

    id = var
    cur = mysql.connection.cursor()
    sql = f"SELECT * FROM db_gempa WHERE `Event ID`='{id}'"
    param = cur.execute(sql)
    par = cur.fetchall()
    par = par[0]
    date,time,lat,long,depth,mag,ket,info = par[1],par[2],par[3],par[4],par[5],par[6],par[7],par[8]
    date = date.strftime('%Y-%m-%d')
    #time = time.strftime('%H:%M:%S')

    print(date)
    
    timeutc = date + ' ' + str(time)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(timeutc[0:19], '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    ot = utc.astimezone(to_zone)
    tgl = ot.strftime("%d")
    bulan = ot.strftime("%b")
    tahun = ot.strftime("%y")
    waktu = ot.strftime("%X")
    bujur = ('%.2f') % float(long)
    depth = ('%.0f') % float(depth)
    if float(lat) > 0:
        NS = "LU"
        ltg = ('%.2f') % float(lat)
    else:
        NS = "LS"
        ltg = ('%.2f') % abs(float(lat))
    mag = ('%.1f') % float(mag)
    keterangan = ket.split()
    min_jarak = keterangan[0]
    arah = keterangan[2]
    minkota = keterangan[3]

    if len(info) > 3:
        param = ('Info Gempa Mag:' + mag + ', ' + tgl + '-' + bulan + '-' + tahun + ' ' + waktu +
                ' WIT, Lok: ' + ltg + ' ' + NS + ', ' + bujur + ' BT (' + min_jarak + ' km ' +
                arah +' '+ minkota + '), Kedlmn:' + depth + ' Km, '+info+' ::BMKG-TNT')
    else:
        param = ('Info Gempa Mag:' + mag + ', ' + tgl + '-' + bulan + '-' + tahun + ' ' + waktu +
                ' WIT, Lok: ' + ltg + ' ' + NS + ', ' + bujur + ' BT (' + min_jarak + ' km ' +
                arah +' '+ minkota + '), Kedlmn:' + depth + ' Km ::BMKG-TNT')
    return param
    

    
if __name__ == "__main__":
	app.run(debug=True)
