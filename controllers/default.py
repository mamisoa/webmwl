# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from mwlarcinterface import MwlInterface
from gluon.contrib import simplejson
import os

def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def get_mwl():
    print(request.vars)
    print(request.vars.date)
    print(request.vars.status)
    print(request.vars.page)
    print(request.vars.pageSize)
    filter = {}
    filter['page_size'] = request.vars.pageSize
    filter['offset'] = int(request.vars.pageSize) * (int(request.vars.page) -1)
    filter['status'] = request.vars.status
    filter['search'] = request.vars.search
    filter['modality'] = request.vars.modality
    filter['scheduled_date'] = request.vars.date.replace('-','')
    print (filter)
    mwl = MwlInterface()
    result = mwl.get_mwl(filter)
    print(result)
    return response.json({'result': result})

def del_mwl():
    print(request.vars.studyUid)
    print(request.vars.spsId)
    mwl = MwlInterface()
    mwl.del_mwl(request.vars.studyUid,request.vars.spsId)
    return response.json({'result': 'success'})

def save_mwl():
    print(request.vars)
    worklist = simplejson.loads(request.body.read())
    print(worklist)
    mwl = MwlInterface()
    sample_wl_folder = os.path.join(request.folder, 'modules')
    result = mwl.create_patient_and_worklist(sample_wl_folder,worklist)
    return response.json(result)

def get_stations():
    if request.vars.search_str:
        search_str = request.vars.search_str
        rows = db(db.station.name.contains(search_str) |
                db.station.modality.contains(search_str) |
                db.station.AE_title.contains(search_str)).select(orderby=db.station.created_on)
    else:
        rows = db(db.station).select(orderby=db.station.created_on)
    return response.json({'result': rows})

def get_procedures():
    if request.vars.search_str:
        search_str = request.vars.search_str
        rows = db(db.imaging_procedure.procedure_id.contains(search_str) |
                db.imaging_procedure.procedure_description.contains(search_str) |
                db.imaging_procedure.modality.contains(search_str)).select(orderby=~db.imaging_procedure.created_on)
    else:
        rows = db(db.imaging_procedure).select(orderby=db.imaging_procedure.created_on)
    return response.json({'result': rows})

def get_patients():
    if request.vars.search_str:
        search_str = request.vars.search_str
        rows = db(db.patient.first_name.contains(search_str) |
            db.patient.last_name.contains(search_str) |
            db.patient.patient_id.contains(search_str)).select(orderby=~db.patient.created_on)
    else:
        rows = db(db.patient).select(orderby=db.patient.created_on)
    return response.json({"result":rows})

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
