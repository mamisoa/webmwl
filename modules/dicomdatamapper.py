from pydicom.dataset import Dataset
from pydicom.dataelem import DataElement
from pydicom.valuerep import PersonName
import pydicom
import string, random
import os

def parse_person_name(name):
    name_components = name.split('^')
    if len(name_components) > 1 :
        return (name_components[0],name_components[1])
    return (name_components[0],'')
def parse_dicom_date(dtString):
    return dtString[:4]+ '-' + dtString[4:6] + '-' + dtString[6:8]

def change_date_to_dicom_format(dateString):
    dds = dateString.replace('-','')
    return dds

def read_wl_file(filename):
    sample_ds = pydicom.dcmread(filename)
    print(sample_ds)
    return sample_ds

def convert_to_dataset(json_obj):
    ds = Dataset()
    for key in json_obj:
        obj = json_obj[key]
        #print "*" , key, obj
        val = ''
        if 'Value' in obj:
            val = obj['Value']
        if obj['vr'] == 'SQ' and val != '' :
            child_ds_list = []
            for val_item in val:
                child_ds = convert_to_dataset(val_item)
                child_ds_list.append(child_ds)
            #print (child_ds_list)
            #print "Creating SQ Element....."
            delem = DataElement(key,obj['vr'],child_ds_list)
            ds.add(delem)
        else:
            if val != '':
                val = val[0]
            delem = DataElement(key,obj['vr'],val)
            ds.add(delem)
            #print delem
    return ds

def convert_dataset_to_json(ds):
    print 'Convert data set to json ------'
    json_obj={}
    for elem in ds:
        print (elem)
        tag = "{0:04x}".format(elem.tag.group)+"{0:04x}".format(elem.tag.element)
        #print tag
        if elem.VR == 'SQ':
            val = []
            for item in elem.value:
                val.append(convert_dataset_to_json(item))
        else:
            val = [elem.value]
        json_obj[tag]={'vr':elem.VR,'Value':val}
    print 'Conversion complete ****'
    return json_obj
def fill_patient_info(ds, mwl_item):
    mwl_item['patient'] = {
    'last_name': '',
    'first_name': '',
    'gender': '',
    'dob': '',
    'weight': '',
    'patient_id': '',
    'patient_size':''
    }

    if 'PatientName' in ds:
        val = ds.PatientName['Alphabetic']
        names = parse_person_name(val)
        mwl_item['patient']['last_name'] = names[0]
        mwl_item['patient']['first_name'] = names[1]
    if 'PatientID' in ds:
        val = ds.PatientID
        mwl_item['patient']['patient_id'] = val
    if 'PatientBirthDate' in ds:
        val = ds.PatientBirthDate
        mwl_item['patient']['dob'] = parse_dicom_date(val)
    if 'PatientSex' in ds:
        val = ds.PatientSex
        mwl_item['patient']['gender'] = 'Male' if val == 'M' else 'Female'
#####################################################################################
# Methods to convert worklist object to Dicom Object
#####################################################################################
def fill_patient_details_from_mwl(mwl_ds,worklist):
    patientname = worklist['patient']['last_name'] + '^' + worklist['patient']['first_name']
    mwl_ds[0x10,0x10].value = PersonName(str(patientname))
    mwl_ds[0x10,0x20].value = worklist['patient']['patient_id']
    mwl_ds[0x10,0x30].value = change_date_to_dicom_format(worklist['patient']['dob'])
    mwl_ds[0x10,0x40].value = 'M' if worklist['patient']['gender'] == 'Male' else 'F'

def fill_isr_details_from_mwl(mwl_ds, worklist):
    mwl_ds[0x08,0x50].value = worklist['isr']['accession_number']
    mwl_ds[0x32,0x1032].value = PersonName(str(worklist['isr']['requesting_physician']))
    #mwl_ds[0x08,0x50] = worklist.isr.accessionNumber

def fill_sps_details_from_mwl(mwl_ds, worklist):
    sps_seq = mwl_ds[0x40,0x100][0]
    sps_seq[0x08,0x60].value = worklist['sps']['modality']
    sps_seq[0x40,0x01].value = worklist['sps']['station_aet']
    sps_seq[0x40,0x10].value = worklist['sps']['station_name']
    alpha = string.ascii_uppercase
    num = string.digits
    id = ''.join(random.choice(alpha + num) for _ in range(7))
    sps_seq[0x40,0x09].value = 'SPD' + id
    del sps_seq[0x40,0x09]
    sps_seq[0x40,0x07].value = worklist['proc_info']['requested_proc_desc']
    sps_seq[0x40,0x02].value = change_date_to_dicom_format(worklist['sps']['start_date'])
    #sps_seq[0x08,0x60] = worklist.sps.modality

def fill_procedure_details_from_mwl(mwl_ds, worklist):
    mwl_ds[0x40,0x1001].value = worklist['proc_info']['proc_id']
    mwl_ds[0x32,0x1060].value = worklist['proc_info']['requested_proc_desc']
    del mwl_ds[0x20,0x0d]

###########################################################################################

def fill_isr_info(ds, mwl_item):
    mwl_item['isr'] = {
        'accession_number': '',
        'requesting_physician': '',
        'referring_physician': ''
    }
    if 'ReferringPhysicianName' in ds:
        if 'Alphabetic' in ds.ReferringPhysicianName:
            val = ds.ReferringPhysicianName['Alphabetic']
        else:
            val = ds.ReferringPhysicianName
        #val = ds.ReferringPhysicianName['Alphabetic']
        names = parse_person_name(val)
        mwl_item['isr']['referring_physician'] = names[0] + ' ' +names[1]
    if 'RequestingPhysician' in ds:
        if 'Alphabetic' in ds.RequestingPhysician:
            val = ds.RequestingPhysician['Alphabetic']
        else:
            val = ds.RequestingPhysician
        names = parse_person_name(val)
        mwl_item['isr']['requesting_physician'] = names[0] + ' ' + names[1]
    if 'AccessionNumber' in ds:
        val = ds.AccessionNumber
        mwl_item['isr']['accession_number'] = val

def fill_sps_info(ds, mwl_item):

    mwl_item['sps'] = {
        'modality': '',
        'station_aet': '',
        'station_name': '',
        'start_date':'',
        'sps_id': '',
        'sps_desc':'',
        'status':''
    }
    sps = ds[0x0040,0x0100].value[0]
    #print sps
    if 'Modality' in sps:
        val = sps.Modality
        mwl_item['sps']['modality'] = val
    if 'ScheduledStationAETitle' in sps:
        val = sps.ScheduledStationAETitle
        mwl_item['sps']['station_aet'] = val
    if 'ScheduledStationName' in sps:
        val = sps.ScheduledStationName
        mwl_item['sps']['station_name'] = val
    if 'ScheduledProcedureStepStartDate' in sps:
        val = sps.ScheduledProcedureStepStartDate
        mwl_item['sps']['start_date'] = parse_dicom_date(val)
    if 'ScheduledProcedureStepID' in sps:
        val = sps.ScheduledProcedureStepID
        mwl_item['sps']['sps_id'] = val
    if 'ScheduledProcedureStepDescription' in sps:
        val = sps.ScheduledProcedureStepDescription
        mwl_item['sps']['sps_desc'] = val
    if 'ScheduledProcedureStepStatus' in sps:
        val = sps.ScheduledProcedureStepStatus
        mwl_item['sps']['status'] = val

def fill_proc_info(ds, mwl_item):
    mwl_item['proc_info'] = {
        'requested_proc_desc': '',
        'proc_id':'',
        'study_uid':''
    }
    if 'RequestedProcedureDescription' in ds:
        val = ds.RequestedProcedureDescription
        mwl_item['proc_info']['requested_proc_desc'] = val
    if 'RequestedProcedureID' in ds:
        val = ds.RequestedProcedureID
        mwl_item['proc_info']['proc_id'] = val
    if 'StudyInstanceUID' in ds:
        val = ds.StudyInstanceUID
        mwl_item['proc_info']['study_uid'] = val



def from_worklist_get_patient_only(sample_wl_folder, worklist):
    ds = read_wl_file(os.path.join(sample_wl_folder,'wklist1.wl'))
    fill_patient_details_from_mwl(ds,worklist)
    del ds[0x40,0x100]
    del ds[0x32,0x1060]
    del ds[0x32,0x1032]
    del ds[0x40,0x1001]
    del ds[0x40,0x1003]
    del ds[0x08,0x0050]
    del ds[0x20,0x000d]
    del ds[0x08,0x0005]
    #del ds[0x10,0x0020]
    del ds[0x10,0x2000]
    del ds[0x10,0x2110]
    return ds
def from_worklist_json(sample_wl_folder, worklist):
    ds = read_wl_file(os.path.join(sample_wl_folder,'wklist1.wl'))
    fill_patient_details_from_mwl(ds,worklist)
    fill_isr_details_from_mwl(ds,worklist)
    fill_sps_details_from_mwl(ds,worklist)
    fill_procedure_details_from_mwl(ds,worklist)
    print (ds)
    return ds

def from_dicom_json(json_obj):
    mwl_item = {}
    ds = convert_to_dataset(json_obj)
    fill_patient_info(ds,mwl_item)
    fill_isr_info(ds,mwl_item)
    fill_sps_info(ds,mwl_item)
    fill_proc_info(ds,mwl_item)
    print (ds)
    #print (mwl_item)
    return mwl_item

if __name__== '__main__':
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
    ds = from_worklist_json(mwl_item)
    json_obj = convert_dataset_to_json(ds)
    print (json_obj)
