# -*- coding: utf-8 -*-
db.define_table('work_list',
               Field('scheduled_date', 'date'),
               Field('patient', 'reference patient'),
               Field('modality', 'reference modality'),
               Field('status', 'reference status'),
               Field('actions', requires = IS_NOT_EMPTY()),
               Field('procedure_todo', requires = IS_NOT_EMPTY()))
