# -*- coding: utf-8 -*-
db.define_table('imaging_procedure',
               Field('procedure_id', requires = IS_NOT_EMPTY()),
               Field('procedure_description', requires = IS_NOT_EMPTY()),
               Field('procedure_code'),
               Field('procedure_code_meaning'),
               Field('procedure_code_scheme_designator'),
               Field('modality'),
               Field('protocol_code'),
               Field('protocol_code_meaning'),
               Field('protocol_code_scheme_designator'),
               auth.signature)
