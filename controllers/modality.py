# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def listmodality():
    modalities = db(db.modality).select()
    return locals()

def addmodality():
    form = SQLFORM(db.modality).process()
    if form.accepted:
        redirect(URL('listmodality'))
    return locals()
