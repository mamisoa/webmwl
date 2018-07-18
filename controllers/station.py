
Items_Per_Page = 10

def index():
	redirect(URL('liststation'))

def liststation():
	Items_Per_Page = 10
	page = request.args(0, cast=int, default = 1)
	stop = page*Items_Per_Page
	start = stop - Items_Per_Page
	total_entries = len(db(db.station).select())
	search_str = request.vars.search_str
	if request.vars.search_str:
		search_str = request.vars.search_str
		rows = db(db.station.name.contains(search_str) |
				db.station.modality.contains(search_str) |
				db.station.AE_title.contains(search_str)).select(orderby=~db.station.created_on,limitby=(start,stop))
		total_entries = len(rows)
	else:
		rows = db(db.station).select(orderby=db.station.created_on,limitby=(start,stop))
	if total_entries % Items_Per_Page > 0:
		total_entries = (total_entries / Items_Per_Page) + 1
	else:
		total_entries = (total_entries / Items_Per_Page)
	for i in range(len(rows)):
		rows[i]['index'] = Items_Per_Page*(page-1)+(i+1)
	return locals()

def addstation():
	name = request.vars.name
	modality = request.vars.modality
	ae_title = request.vars.AE_title
	dcm_compliant = 'DICOM_Compliant' in request.vars
	if len(request.vars)>0:
		db.station.insert(name=name, modality=modality,AE_title=ae_title, DICOM_Compliant=dcm_compliant)
		redirect(URL('liststation'))
	modalities = ["CR", "CT", "DX", "MR", "MG", "NM","US", "ES", "EPS","ECG","BMD","BI","PT","OPT", "OT", "RF", "XA"]
	return locals()

def editstation():
	if len(request.vars) <=1 :
		id = request.vars.id
		station = db.station(id)
		modalities = ["CR", "CT", "DX", "MR", "MG", "NM","US", "ES", "EPS","ECG","BMD","BI","PT","OPT", "OT", "RF", "XA"]
		return locals()
	else:
		id = request.args(0)
		station = db(db.station.id==id).select().first()
		station.update_record(name=request.vars.name,
			modality=request.vars.modality,
			AE_title=request.vars.AE_title)
		redirect(URL('liststation'))
		return locals()

def deletestation():
	id = request.vars.id
	station = db(db.station.id==id).delete()
	session.flash = "Deleted successfully!"
	redirect(URL('liststation'))
	return locals()
