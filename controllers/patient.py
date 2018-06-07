# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def listpatient():
    patients = db(db.patient).select()
    return locals()

def addpatient():
    form = SQLFORM(db.patient).process()
    if form.accepted:
        redirect(URL('listpatient'))
    return locals()
