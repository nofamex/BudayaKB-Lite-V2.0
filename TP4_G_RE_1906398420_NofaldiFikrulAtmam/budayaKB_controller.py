#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)

Last update: 23 November 2019

"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()


#merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")

	elif request.method == "POST":
		f = request.files['file']
		global databasefilename
		databasefilename=f.filename
		result_impor=budayaData.importFromCSV(f.filename)
		budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
		return render_template("imporBudaya.html", result=result_impor, fname=f.filename)

@app.route('/tambahBudaya', methods=["GET","POST"])
def tambah():
	if request.method == "GET":
		return render_template("tambahBudaya.html")
	elif request.method == "POST":
		aNama = request.form["namabudaya"]
		aTipe = request.form["tipe"]
		aProv = request.form["provinsi"]
		aURL = request.form["url"]

		if databasefilename!="":
			hasil = budayaData.tambah(aNama,aTipe,aProv,aURL)
			budayaData.exportToCSV(databasefilename)
			return render_template("tambahBudaya.html",result=hasil,nama=aNama)
		else:
			return render_template("imporBudaya.html")


@app.route('/ubahBudaya', methods=["GET",'POST'])
def ubah():
	if request.method == "GET":
		return render_template("ubahBudaya.html")
	elif request.method == "POST":
		aNama = request.form["namabudaya"]
		aTipe = request.form["tipe"]
		aProv = request.form["provinsi"]
		aURL = request.form["url"]
	
		if databasefilename!="":
			hasil = budayaData.ubah(aNama,aTipe,aProv,aURL)
			budayaData.exportToCSV(databasefilename)
			return render_template("ubahBudaya.html",result=hasil,nama=aNama)
		else:
			return render_template("imporBudaya.html")

@app.route('/hapusBudaya', methods=["GET","POST"])
def hapus():	
	if request.method == "GET":
		return render_template("hapusBudaya.html")
	elif request.method == "POST":
		aName = request.form["namabudaya"]
	
		if databasefilename!="":
			hasil = budayaData.hapus(aName)
			budayaData.exportToCSV(databasefilename)
			return render_template("hapusBudaya.html",result=hasil,nama=aName)
		else:
			return render_template("imporBudaya.html")

@app.route('/cariBudaya', methods=["GET","POST"])
def cari():
	if request.method == "GET":
		return render_template("cariBudaya.html")
	elif request.method == "POST":
		tipecari = request.form['jenis']
		ingin = request.form['nama']
		if databasefilename!="":
			if tipecari == "Nama Budaya":
				cari = budayaData.cariByNama(ingin)
				return render_template('cariBudaya.html',result=cari,nama=ingin,tipe=tipecari)
			elif tipecari == "Tipe Budaya":
				tipe = budayaData.cariByTipe(ingin)
				return render_template('cariBudaya.html', result=tipe,nama=ingin,tipe=tipecari)
			elif tipecari == "Provinsi Budaya":
				prov = budayaData.cariByProv(ingin)
				return render_template('cariBudaya.html', result=prov,nama=ingin,tipe=tipecari)
		else:
			return render_template("imporBudaya.html")

@app.route('/statsBudaya', methods=["GET","POST"])
def stat():
	if request.method == "GET":
		return render_template("statsBudaya.html")
	elif request.method == "POST":
		tipe = request.form['jenis']
		if databasefilename != "":
			if tipe == "All":
				stat = budayaData.stat()
				return render_template("statsBudaya.html",result=stat,tipex=tipe,file=databasefilename)
			if tipe == "Tipe":
				stat = budayaData.statByTipe()
				return render_template("statsBudaya.html",result=stat,tipex=tipe)
			if tipe == "Provinsi":
				stat = budayaData.statByProv()
				return render_template("statsBudaya.html",result=stat,tipex=tipe)
		else:
			return render_template("imporBudaya.html")
# run main app
if __name__ == "__main__":
	app.run(debug=True)