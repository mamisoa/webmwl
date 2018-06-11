
Items_Per_Page = 10

def index():
	redirect(URL('listprocedure'))

def listprocedure():
	Items_Per_Page = 10
	page = request.args(0, cast=int, default = 1)
	stop = page*Items_Per_Page
	start = stop - Items_Per_Page
	total_entries = len(db(db.imaging_procedure).select())
	if total_entries % Items_Per_Page > 0:
		total_entries = (total_entries / Items_Per_Page) + 1
	else:
		total_entries = (total_entries / Items_Per_Page)
	search_str = request.vars.search_str
	if request.vars.search_str:
		search_str = request.vars.search_str
		rows = db(db.imaging_procedure.procedure_id.contains(search_str)).select(orderby=~db.imaging_procedure.created_on,limitby=(start,stop))
	else:
		rows = db(db.imaging_procedure).select(orderby=db.imaging_procedure.created_on,limitby=(start,stop))
	return locals()

def addprocedure():
	modalities = ["modality1", "modality2", "modality3", "modality4"]
	procedure_id = request.vars.procedure_id
	procedure_desc = request.vars.procedure_desc
	procedure_code = request.vars.procedure_code
	procedure_code_meaning = request.vars.procedure_code_meaning
	procedure_code_scheme_designator = request.vars.procedure_code_scheme_designator
	modality = request.vars.modality
	protocol_code = request.vars.protocol_code
	protocol_code_meaning = request.vars.protocol_code_meaning
	protocol_code_scheme_designator = request.vars.protocol_code_scheme_designator
	if len(request.vars)>0:
		db.imaging_procedure.insert(procedure_id=procedure_id, procedure_description=procedure_desc,
					procedure_code=procedure_code, procedure_code_meaning=procedure_code_meaning,
					procedure_code_scheme_designator=procedure_code_scheme_designator, modality=modality,
					protocol_code=protocol_code,protocol_code_meaning=protocol_code_meaning,
					protocol_code_scheme_designator=protocol_code_scheme_designator)
		redirect(URL('listprocedure'))
	return locals()

def deleteprocedure():
	id = request.vars.id
	procedure = db(db.imaging_procedure.id==id).delete()
	session.flash = "Deleted successfully!"
	redirect(URL('listprocedure'))
	return locals()

def editprocedure():
	modalities = ["modality1", "modality2", "modality3", "modality4"]
	if len(request.vars) <=1 :
		id = request.vars.id
		procedure = db.imaging_procedure(id)
		return locals()
	else:
		id = request.args(0)
		procedure = db(db.imaging_procedure.id==id).select().first()
		procedure_id = request.vars.procedure_id
		procedure_desc = request.vars.procedure_desc
		procedure_code = request.vars.procedure_code
		procedure_code_meaning = request.vars.procedure_code_meaning
		procedure_code_scheme_designator = request.vars.procedure_code_scheme_designator
		modality = request.vars.modality
		protocol_code = request.vars.protocol_code
		protocol_code_meaning = request.vars.protocol_code_meaning
		protocol_code_scheme_designator = request.vars.protocol_code_scheme_designator
		procedure.update_record(procedure_id=procedure_id, procedure_description=procedure_desc,
					procedure_code=procedure_code, procedure_code_meaning=procedure_code_meaning,
					procedure_code_scheme_designator=procedure_code_scheme_designator, modality=modality,
					protocol_code=protocol_code,protocol_code_meaning=protocol_code_meaning,
					protocol_code_scheme_designator=protocol_code_scheme_designator)
		redirect(URL('listprocedure'))
		return locals()