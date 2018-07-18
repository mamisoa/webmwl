# -*- coding: utf-8 -*-
db.define_table('station',
               Field('name', requires = IS_NOT_EMPTY()),
               Field('modality', requires = IS_NOT_EMPTY()),
               Field('AE_title', requires = IS_NOT_EMPTY()),
               Field('DICOM_Compliant','boolean', default=False),
               auth.signature)

db.define_table('arcconfig',
               Field('arc_hostname', requires = IS_NOT_EMPTY(), defaults="localhost"),
               Field('arc_port', requires = IS_NOT_EMPTY(), defaults="8080"),
               Field('arc_ae_title', requires = IS_NOT_EMPTY(), defaults="DCM4CHEE"),
               auth.signature)
