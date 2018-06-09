from pydicom.dataset import Dataset
from pydicom.dataelem import DataElement


def parse_person_name(name):
    name_components = name.split('^')
    if len(name_components) > 1 :
        return (name_components[0],name_components[1])
    return (name_components[0],'')
def parse_dicom_date(dtString):
    return dtString[:4]+ '-' + dtString[4:6] + '-' + dtString[6:8]


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

def fill_isr_info(ds, mwl_item):
    mwl_item['isr'] = {
        'accession_number': '',
        'requesting_physician': '',
        'referring_physician': ''
    }
    if 'ReferringPhysicianName' in ds:
        val = ds.ReferringPhysicianName['Alphabetic']
        names = parse_person_name(val)
        mwl_item['isr']['referring_physician'] = names[0] + ' ' +names[1]
    if 'RequestingPhysician' in ds:
        val = ds.RequestingPhysician['Alphabetic']
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
        mwl_item['sps']['start_date'] = val
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


def from_dicom_json(json_obj):
    mwl_item = {}
    #print (json_obj)
    #ds = Dataset(json_obj)
    #fill_patient_info(ds,mwl_item)
    #ds.walk(walk_callback,True)
    ds = convert_to_dataset(json_obj)
    fill_patient_info(ds,mwl_item)
    fill_isr_info(ds,mwl_item)
    fill_sps_info(ds,mwl_item)
    fill_proc_info(ds,mwl_item)
    print (ds)
    #print (mwl_item)
    return mwl_item
