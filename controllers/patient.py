
Items_Per_Page = 10

def index():
	redirect(URL('listpatient'))

def cal_age(born):
	from datetime import datetime
	age = (datetime.now().date() - born).days / 365 
	age_str = str(age) + ' years'
	if age < 1:
		age = (datetime.now().date() - born).days / 30
		age_str = str(age) + ' months'
		if age < 1:
			age = (datetime.now().date() - born).days
			age_str = str(age) + ' days'
			if age < 1:
				age_str = "Invalid age"

	return age_str

def listpatient():
	sort = 0
	Items_Per_Page = 10
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
	search_str = request.vars.search_str

	if request.vars.search_str:
		search_str = request.vars.search_str
		rows = db(db.patient.first_name.contains(search_str) | 
			db.patient.last_name.contains(search_str)).select(orderby=~db.patient.created_on,limitby=(start,stop))
	else:
		rows = db(db.patient).select(orderby=db.patient.created_on,limitby=(start,stop))
	for row in rows:
		row.age = cal_age(row.birth_date)
	return locals()

def addpatient():
	first_name = request.vars.first_name
	last_name = request.vars.last_name
	birth_date = request.vars.birth_date
	gender = request.vars.gender
	weight = request.vars.weight
	patient_size = request.vars.patient_size
	patient_id = request.vars.patient_id
	if len(request.vars)>0:
		db.patient.insert(first_name=first_name, last_name=last_name,
					birth_date=birth_date, gender=gender,
					patient_size=patient_size, weight=weight, 
					patient_id = patient_id)
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
			birth_date=request.vars.birth_date,
			patient_id = request.vars.patient_id)
		redirect(URL('listpatient'))
		return locals()