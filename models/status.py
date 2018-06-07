# -*- coding: utf-8 -*-
db.define_table('status',
               Field('name', requires = IS_NOT_EMPTY()))
