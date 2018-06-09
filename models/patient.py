# -*- coding: utf-8 -*-
db.define_table('patient',
               Field('first_name', requires = IS_NOT_EMPTY()),
               Field('last_name', requires = IS_NOT_EMPTY()),
               Field('birth_date','date'),
               Field('gender'),
               Field('weight'),
               Field('patient_size'),
               auth.signature)
