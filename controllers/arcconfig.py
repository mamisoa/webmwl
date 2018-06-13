
Items_Per_Page = 10

def index():
	redirect(URL('listarcconfig'))

def listarcconfig():
	rows = db(db.arcconfig).select()
	if len(rows) < 1:
		db.arcconfig.insert(arc_hostname="localhost",
					arc_port="8080",
					arc_ae_title="DCM4CHEE")
		redirect(URL('listarcconfig'))
	return locals()

def editarcconfig():
	if len(request.vars) <=1 :
		id = request.vars.id
		arc_config = db.arcconfig(id)
		return locals()
	else:
		id = request.args(0)
		arc_config = db(db.arcconfig.id==id).select().first()
		arc_config.update_record(arc_hostname=request.vars.arc_hostname,
			arc_port=request.vars.arc_port,
			arc_ae_title=request.vars.arc_ae_title)
		redirect(URL('listarcconfig'))
		return locals()

def deletearcconfig():
	id = request.vars.id
	station = db(db.arcconfig.id==id).delete()
	session.flash = "Deleted successfully!"
	redirect(URL('listarcconfig'))
	return locals()