import requests
import json
from dicomdatamapper import from_dicom_json, from_worklist_json, convert_dataset_to_json, from_worklist_get_patient_only
class MwlInterface:
    BASE_URL = 'http://localhost:8080/dcm4chee-arc/'
    DCM_FIELD_MAP = {
        'patient_name': '00100010',
        'modality': '00400100.00080060',
        'status': '00400100.00400020',
        'scheduled_date': '00400100.00400002'
    }
    def __init__(self, arc_config):
        self.BASE_URL = 'http://' + arc_config['host'] + ':' + arc_config['port'] + '/dcm4chee-arc/'
        self.AET_URL = self.BASE_URL + 'aets/' + arc_config['ae_title']
    def get_aes(self):
        aes_url = self.BASE_URL + 'aes'
        response = requests.get(aes_url)
        aes_list = response.json()
        for ae in aes_list:
            print unicode(ae)
    def get_device(self, device):
        dev_url = self.BASE_URL + 'devices/' + device
        response = requests.get(dev_url)
        dev = response.json()
        print(json.dumps(dev))
        #print (unicode(dev))
    def map_field_to_dicom_tag(self, field, search):
        if field == 'patient_name':
            return '00100010'
    def create_filter(self, search, filter):
        if filter is not None:
            if 'page_size' in filter:
                search['limit'] = filter['page_size']
            if 'offset' in filter:
                search['offset'] = filter['offset']
            if 'status' in filter:
                search[self.DCM_FIELD_MAP['status']] = filter['status']
            if 'scheduled_date' in filter:
                search[self.DCM_FIELD_MAP['scheduled_date']] = filter['scheduled_date']
            if 'search' in filter and filter['search'] != '':
                search[self.DCM_FIELD_MAP['patient_name']] = filter['search']
                search['fuzzymatching'] = 'true'
            if 'modality' in filter and filter['modality'] != 'ALL':
                search[self.DCM_FIELD_MAP['modality']] = filter['modality']
    def get_count(self, filter):
        search = {}
        self.create_filter(search,filter)
        mwl_url = self.AET_URL + '/rs/mwlitems/count'
        response = requests.get(mwl_url, params=search)
        if response.status_code == 204 :
            return {'count':0}
        if response.status_code >= 400:
            print (response.text)
            return {'count':0}
        count = response.json()
        return count
    def get_mwl(self, filter=None):
        count = self.get_count(filter)
        print (str(count))
        if count['count'] == 0:
            print "Count has returned as zero!!"
            return {
                'count': 0,
                'items': []
            }
        print ('Total number of results = '+ str(count['count']))
        search = {'includefield': 'all'}
        self.create_filter(search,filter)
        #mwl_url = self.BASE_URL + 'aets/DCM4CHEE/rs/mwlitems'
        mwl_url = self.AET_URL + '/rs/mwlitems'
        #search['00400100.00080060'] = 'MR'
        print (search)
        response = requests.get(mwl_url, params=search)
        print (unicode(response))
        if response.status_code == 204 :
            return []
        if response.status_code >= 400:
            print (response.text)
            return []
        mwl_json_items = response.json()
        mwl_items = []
        print("Returned results ="+ str(len(mwl_json_items)))
        for item in mwl_json_items:
            #print (item)
            mwl_item = from_dicom_json(item)
            #print mwl_item
            mwl_items.append(mwl_item)
        #print unicode(mwl_items)
        return {
            'count': count['count'],
            'items': mwl_items
            }
    def del_mwl(self, studyUid, spsId):
        #mwl_url = self.BASE_URL + 'aets/DCM4CHEE/rs/mwlitems/' + studyUid + '/' + spsId
        mwl_url = self.AET_URL + '/rs/mwlitems/' + studyUid + '/' + spsId
        requests.delete(mwl_url)

    def create_mwl(self, sample_wl_folder, worklist):
        wl_ds = from_worklist_json(sample_wl_folder, worklist)
        wl_json = convert_dataset_to_json(wl_ds)
        print (wl_json)
        #mwl_url = self.BASE_URL + 'aets/DCM4CHEE/rs/mwlitems'
        mwl_url = self.AET_URL + '/rs/mwlitems'
        response = requests.post(mwl_url, json=wl_json)
        print unicode(response)
        print unicode(response.text)
        return {'result': 'success'}
    def create_patient(self,sample_wl_folder, worklist):
        wl_ds = from_worklist_get_patient_only(sample_wl_folder,worklist)
        wl_json = convert_dataset_to_json(wl_ds)
        print (wl_json)
        #mwl_url = self.BASE_URL + 'aets/DCM4CHEE/rs/patients/'+worklist['patient']['patient_id']
        mwl_url = self.AET_URL + '/rs/patients/'+worklist['patient']['patient_id']
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
    arc_if = MwlInterface({
        'host': 'localhost',
        'ae_title': 'DCM4CHEE',
        'port': '8080'
    })
    #arc_if.get_device('dcm4chee-arc')
    #print()
    #pid = arc_if.create_patient(mwl_item)
    # mwl_item['patient']['patient_id'] = pid
    #arc_if.create_mwl(mwl_item)
    #print(arc_if.get_mwl({'scheduled_date':'20180611'}))
    print(arc_if.get_mwl({"status":"SCHEDULED"}))
    #arc_if.del_mwl('2.25.247228648750766432344279402705598180830', 'SPS-00000001')
