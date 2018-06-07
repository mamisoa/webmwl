# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def liststatus():
    status_list = db(db.status).select()
    return locals()

def addstatus():
    form = SQLFORM(db.status).process()
    if form.accepted:
        redirect(URL('liststatus'))
    return locals()
