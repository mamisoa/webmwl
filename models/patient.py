# -*- coding: utf-8 -*-
db.define_table('patient',
               Field('first_name', requires = IS_NOT_EMPTY()),
               Field('last_name', requires = IS_NOT_EMPTY()),
               Field('age','integer'),
               Field('gender'))
