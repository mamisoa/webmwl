# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def listgender():
    genders = db(db.gender).select()
    return locals()

def addgender():
    form = SQLFORM(db.gender).process()
    if form.accepted:
        redirect(URL('listgender'))
    return locals()
