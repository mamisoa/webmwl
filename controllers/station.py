
Items_Per_Page = 10

def index():
	redirect(URL('liststation'))

def liststation():
	Items_Per_Page = 10
	page = request.args(0, cast=int, default = 1)
	stop = page*Items_Per_Page
	start = stop - Items_Per_Page

	total_entries = len(db(db.station).select())

	if total_entries % Items_Per_Page > 0:
		total_entries = (total_entries / Items_Per_Page) + 1
	else:
		total_entries = (total_entries / Items_Per_Page)

	search_str = request.vars.search_str

	if request.vars.search_str:
		search_str = request.vars.search_str
		rows = db(db.station.name.contains(search_str)).select(orderby=~db.station.created_on,limitby=(start,stop))
	else:
		rows = db(db.station).select(orderby=db.station.created_on,limitby=(start,stop))
	return locals()

def addstation():
	name = request.vars.name
	modality = request.vars.modality
	ae_title = request.vars.AE_title
	if len(request.vars)>0:
		db.station.insert(name=name, modality=modality,AE_title=ae_title)
		redirect(URL('liststation'))
	modalities = ["modality1", "modality2", "modality3", "modality4"]
	return locals()

def editstation():
	if len(request.vars) <=1 :
		id = request.vars.id
		station = db.station(id)
		modalities = ["modality1", "modality2", "modality3", "modality4"]
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