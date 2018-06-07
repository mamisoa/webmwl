# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def worklist():
    worklists = db(db.work_list).select()
    return locals()

def addworklist():
    #form = SQLFORM(db.work_list).process()
    form = SQLFORM(db.work_list).process()
    if form.accepted:
        redirect(URL('worklist'))
    return locals()
