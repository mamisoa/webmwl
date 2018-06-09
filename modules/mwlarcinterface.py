import requests
from dicomdatamapper import from_dicom_json
class MwlInterface:
    BASE_URL = 'http://localhost:8080/dcm4chee-arc/'
    DCM_FIELD_MAP = {
        'patient_name': '00100010',
        'modality': '00400100.00080060',
        'status': '00400100.00400020',
        'scheduled_date': '00400100.00400002'
    }
    def get_aes(self):
        aes_url = self.BASE_URL + 'aes'
        response = requests.get(aes_url)
        aes_list = response.json()
        for ae in aes_list:
            print unicode(ae)
    def map_field_to_dicom_tag(self, field, search):
        if field == 'patient_name':
            return '00100010'

    def get_mwl(self, filter=None):
        search = {}
        if filter is not None:
            if 'page_size' in filter:
                search['limit'] = filter['page_size']
            if 'offset' in filter:
                search['offset'] = filter['offset']

        mwl_url = self.BASE_URL + 'aets/DCM4CHEE/rs/mwlitems'

        search['00400100.00080060'] = 'MR'
        response = requests.get(mwl_url, params=search)
        print (unicode(response))
        if response.status_code == 204 :
            return []
        mwl_json_items = response.json()
        mwl_items = []
        for item in mwl_json_items:
            mwl_item = from_dicom_json(item)
            print mwl_item
            mwl_items.append(mwl_item)
        print unicode(mwl_items)
        return mwl_items
