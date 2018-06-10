# -*- coding: utf-8 -*-
db.define_table('station',
               Field('name', requires = IS_NOT_EMPTY()),
               Field('modality', requires = IS_NOT_EMPTY()),
               Field('AE_title', requires = IS_NOT_EMPTY()),
               auth.signature)
