# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----

Items_Per_Page = 10
from gluon.tools import Crud

def index():
	sort = 0
	page = request.args(0, cast=int, default = 1)
	stop = page*Items_Per_Page
	start = stop - Items_Per_Page
	req_sort = request.args(1, cast=int, default = 0)

	total_entries = len(db(db.patient).select())
	if total_entries % Items_Per_Page > 0:
		total_entries = (total_entries / Items_Per_Page) + 1
	else:
		total_entries = (total_entries / Items_Per_Page)

	if req_sort == 0:
		rows = db(db.patient).select(orderby=db.patient.created_on,limitby=(start,stop))
	else:
		rows = db(db.patient).select(orderby=~db.patient.created_on,limitby=(start,stop))
	return locals()

def listpatient():
	sort = 0
	page = request.args(0, cast=int, default = 1)
	stop = page*Items_Per_Page
	start = stop - Items_Per_Page
	req_sort = request.args(1, cast=int, default = 0)

	total_entries = len(db(db.patient).select())
	if total_entries % Items_Per_Page > 0:
		total_entries = (total_entries / Items_Per_Page) + 1
	else:
		total_entries = (total_entries / Items_Per_Page)

	if req_sort == 0:
		rows = db(db.patient).select(orderby=db.patient.created_on,limitby=(start,stop))
	else:
		rows = db(db.patient).select(orderby=~db.patient.created_on,limitby=(start,stop))
	return locals()

def list_patient_by_datetime():
	page = request.args(0, cast=int, default = 0)
	start = page*Items_Per_Page
	stop = start + Items_Per_Page
	rows = db(db.patient).select(orderby=~db.patient.created_on,limitby=(start,stop))
	return locals()

def list_patients_by_name():
	page = request.args(0, cast=int, default = 0)
	start = page*Items_Per_Page
	stop = start + Items_Per_Page
	search_str = request.args(1, default="hello")
	rows = db(db.patient.first_name.like('%search_str%', case_sensitive=False)).select(orderby=~db.patient.created_on,limitby=(start,stop))
	#rows = db(db.patient).select(orderby=~db.patient.created_on,limitby=(start,stop))
	return locals()

def addpatient():
	first_name = request.vars.first_name
	last_name = request.vars.last_name
	birth_date = request.vars.birth_date
	gender = request.vars.gender
	weight = request.vars.weight
	patient_size = request.vars.patient_size
	if len(request.vars)>0:
		db.patient.insert(first_name=first_name, last_name=last_name,
					birth_date=birth_date, gender=gender,
					patient_size=patient_size, weight=weight)
		redirect(URL('listpatient'))
	return locals()

def deletepatient():
	id = request.vars.id
	patient = db(db.patient.id==id).delete()
	session.flash = "Deleted successfully!"
	redirect(URL('listpatient'))
	return locals()

def editpatient():
	if len(request.vars) <=1 :
		id = request.vars.id
		patient = db.patient(id)
		return locals()
	else:
		id = request.args(0)
		patient = db(db.patient.id==id).select().first()
		patient.update_record(first_name=request.vars.first_name,
			last_name=request.vars.last_name,
			patient_size=request.vars.patient_size,
			weight=request.vars.weight,
			birth_date=request.vars.birth_date)
		redirect(URL('listpatient'))
		return locals()