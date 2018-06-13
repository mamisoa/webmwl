# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, '#', [
            (T('Design'), False, URL('admin', 'default', 'design/%s' % _app)),
            (T('Controller'), False,
             URL(
                 'admin', 'default', 'edit/%s/controllers/%s.py' % (_app, request.controller))),
            (T('View'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/%s' % (_app, response.view))),
            (T('DB Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/db.py' % _app)),
            (T('Menu Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/menu.py' % _app)),
            (T('Config.ini'), False,
             URL(
                 'admin', 'default', 'edit/%s/private/appconfig.ini' % _app)),
            (T('Layout'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/layout.html' % _app)),
            (T('Stylesheet'), False,
             URL(
                 'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % _app)),
            (T('Database'), False, URL(_app, 'appadmin', 'index')),
            (T('Errors'), False, URL(
                'admin', 'default', 'errors/' + _app)),
            (T('About'), False, URL(
                'admin', 'default', 'about/' + _app)),
        ]),
        ('Patients', False, '#', [
            (T('Add Patinet'), False,
             '/webmwl/patient/addpatient'),
            (T('List Patients'), False, '/webmwl/patient/listpatient'),
        ]),
        (T('Stations'), False, '#', [
            (T('Add Station'), False,
             '/webmwl/station/addstation'),
            (T('List Stations'), False, '/webmwl/station/liststation'),
        ]),
        (T('Procedures'), False, None, [
            (T('Add Procedure'), False,
             '/webmwl/procedure/addprocedure'),
            (T('List Procedures'), False,
             '/webmwl/procedure/listprocedure'),
        ]),
        (T('Arc Config'), False, None, [
            (T('Arc Config'), False,
             '/webmwl/arcconfig/listarcconfig'),
        ]),
    ]

