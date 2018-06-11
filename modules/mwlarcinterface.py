import requests
from dicomdatamapper import from_dicom_json, from_worklist_json, convert_dataset_to_json, from_worklist_get_patient_only
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

        #search['00400100.00080060'] = 'MR'
        response = requests.get(mwl_url, params=search)
        print (unicode(response))
        if response.status_code == 204 :
            return []
        mwl_json_items = response.json()
        mwl_items = []
        for item in mwl_json_items:
            print (item)
            mwl_item = from_dicom_json(item)
            print mwl_item
            mwl_items.append(mwl_item)
        print unicode(mwl_items)
        return mwl_items
    def create_mwl(self, sample_wl_folder, worklist):
        wl_ds = from_worklist_json(sample_wl_folder, worklist)
        wl_json = convert_dataset_to_json(wl_ds)
        print (wl_json)
        mwl_url = self.BASE_URL + 'aets/DCM4CHEE/rs/mwlitems'
        response = requests.post(mwl_url, json=wl_json)
        print unicode(response)
        print unicode(response.text)
        return {'result': 'success'}
    def create_patient(self,sample_wl_folder, worklist):
        wl_ds = from_worklist_get_patient_only(sample_wl_folder,worklist)
        wl_json = convert_dataset_to_json(wl_ds)
        print (wl_json)
        mwl_url = self.BASE_URL + 'aets/DCM4CHEE/rs/patients/'+worklist['patient']['patient_id']
        response = requests.put(mwl_url, json=wl_json)
        print unicode(response)
        print unicode(response.text)
    def create_patient_and_worklist(self, sample_wl_folder, worklist):
        self.create_patient(sample_wl_folder, worklist)
        return self.create_mwl(sample_wl_folder,worklist)

if __name__ == '__main__':
    mwl_item = {}
    mwl_item['patient'] = {
    'last_name': 'Doe',
    'first_name': 'John',
    'gender': 'Male',
    'dob': '1978-10-27',
    'weight': '',
    'patient_id': 'P12345',
    'patient_size':''
    }
    mwl_item['isr'] = {
        'accession_number': 'A123454',
        'requesting_physician': 'David Johnson',
        'referring_physician': 'Shane Warne'
    }
    mwl_item['sps'] = {
        'modality': 'DX',
        'station_aet': 'Definium 1000',
        'station_name': 'DX1',
        'start_date':'2018-06-11',
        'sps_id': 'SPS12345',
        'sps_desc':'SPS Desc',
        'status':'SCHEDULED'
    }
    mwl_item['proc_info'] = {
        'requested_proc_desc': 'RP1',
        'proc_id':'RP0001',
        'study_uid':'1.2.3.4.5.284928943.32434'
    }
    arc_if = MwlInterface()
    pid = arc_if.create_patient(mwl_item)
    # mwl_item['patient']['patient_id'] = pid
    #arc_if.create_mwl(mwl_item)
    print(arc_if.get_mwl())
