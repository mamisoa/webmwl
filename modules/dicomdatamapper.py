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
            if elem.VR == 'DS':
                val=[float(elem.value)]
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
    'patient_size':'',
    'med_alerts': '',
    'allergies': ''
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
    if 'MedicalAlerts' in ds:
        val = ds.MedicalAlerts
        mwl_item['patient']['med_alerts'] = val
    if 'Allergies' in ds:
        val = ds.Allergies
        mwl_item['patient']['allergies'] = val
    if 'PatientWeight' in ds:
        val = ds.PatientWeight
        mwl_item['patient']['weight'] = val
    if 'PatientSize' in ds:
        val = ds.PatientSize
        print('------------------++++++++++++++++')
        print(val)
        mwl_item['patient']['patient_size'] = val
#####################################################################################
# Methods to convert worklist object to Dicom Object
#####################################################################################
def fill_patient_details_from_mwl(mwl_ds,worklist):
    patientname = worklist['patient']['last_name'] + '^' + worklist['patient']['first_name']
    mwl_ds[0x10,0x10].value = PersonName(str(patientname))
    mwl_ds[0x10,0x20].value = worklist['patient']['patient_id']
    mwl_ds[0x10,0x30].value = change_date_to_dicom_format(worklist['patient']['dob'])
    mwl_ds[0x10,0x40].value = 'M' if worklist['patient']['gender'] == 'Male' else 'F'
    mwl_ds[0x10,0x2000].value = worklist['patient']['med_alerts']
    mwl_ds[0x10,0x2110].value = worklist['patient']['allergies']
    if not 'PatientWeight' in mwl_ds:
        if worklist['patient']['weight'] != '':
            mwl_ds.add_new((0x10,0x1030),'DS',float(worklist['patient']['weight']))
    else:
        if worklist['patient']['weight'] != '':
            mwl_ds[0x10,0x1030].value = float(worklist['patient']['weight'])
    if not 'PatientSize' in mwl_ds:
        if worklist['patient']['patient_size'] != '':
            try:
                size_val = float(worklist['patient']['patient_size'])
                mwl_ds.add_new((0x10,0x1020),'DS',size_val)
            except:
                print('Error while parsing patient size')
    else:
        if worklist['patient']['patient_size'] != '':
            try:
                size_val = float(worklist['patient']['patient_size'])
                mwl_ds[0x10,0x1020] = size_val
            except:
                print('Error while parsing patient size')


def fill_isr_details_from_mwl(mwl_ds, worklist):
    mwl_ds[0x08,0x50].value = worklist['isr']['accession_number']
    mwl_ds[0x32,0x1032].value = PersonName(str(worklist['isr']['requesting_physician']))
    #mwl_ds[0x08,0x50] = worklist.isr.accessionNumber

def fill_sps_details_from_mwl(mwl_ds, worklist):
    sps_seq = mwl_ds[0x40,0x100][0]
    sps_seq[0x08,0x60].value = worklist['sps']['modality']
    sps_seq[0x40,0x01].value = worklist['sps']['station_aet']
    sps_seq[0x40,0x10].value = worklist['sps']['station_name']
    if worklist['sps']['sps_id'] == '':
        alpha = string.ascii_uppercase
        num = string.digits
        id = ''.join(random.choice(alpha + num) for _ in range(7))
        sps_seq[0x40,0x09].value = 'SPD' + id
    else:
        sps_seq[0x40,0x09].value = worklist['sps']['sps_id']

    sps_seq[0x40,0x07].value = worklist['proc_info']['requested_proc_desc']
    sps_seq[0x40,0x02].value = change_date_to_dicom_format(worklist['sps']['start_date'])
    sps_seq[0x0032, 0x1070].value = worklist['sps']['contrast_agent']
    sps_seq[0x0040, 0x0400].value = worklist['sps']['comments']
    sps_seq[0x0040, 0x0006].value = PersonName(str( worklist['sps']['operator']))
    sps_seq[0x0040, 0x0012].value = worklist['sps']['pre_meds']
    sps_seq[0x40,0x03].value = worklist['sps']['start_time']
    if worklist['sps']['protocol_code'] != '':
        protocol_seq = Dataset()
        protocol_seq.CodeValue = worklist['sps']['protocol_code']
        protocol_seq.CodingSchemeDesignator = worklist['sps']['protocol_code_scheme_designator']
        protocol_seq.CodeMeaning = worklist['sps']['protocol_code_meaning']
        sps_seq.ScheduledProtocolCodeSequence = [protocol_seq]
    #sps_seq[0x08,0x60] = worklist.sps.modality

def fill_procedure_details_from_mwl(mwl_ds, worklist):
    mwl_ds[0x40,0x1001].value = worklist['proc_info']['proc_id']
    mwl_ds[0x40,0x1003].value = worklist['proc_info']['proc_priority']
    mwl_ds[0x32,0x1060].value = worklist['proc_info']['requested_proc_desc']
    if worklist['proc_info']['study_uid'] == '':
        mwl_ds[0x20,0x0d].value = pydicom.uid.generate_uid()
    else:
        mwl_ds[0x20,0x0d].value = worklist['proc_info']['study_uid']
    if not 'ReasonForTheRequestedProcedure' in mwl_ds:
        mwl_ds.add_new((0x40,0x1002),'LO',worklist['proc_info']['request_reason'])
    else:
        mwl_ds[0x40,0x1002].value = worklist['proc_info']['request_reason']
    if worklist['proc_info']['procedure_code'] != '':
        protocol_seq = Dataset()
        protocol_seq.CodeValue = worklist['proc_info']['procedure_code']
        protocol_seq.CodingSchemeDesignator = worklist['proc_info']['proc_scheme_designator']
        protocol_seq.CodeMeaning = worklist['proc_info']['procedure_code_meaning']
        mwl_ds.RequestedProcedureCodeSequence = [protocol_seq]

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
        'status':'',
        'contrast_agent': '',
        'pre_meds': '',
        'comments': '',
        'operator': '',
        'protocol_code': '',
        'protocol_code_meaning': '',
        'protocol_code_scheme_designator': ''
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
    if 'ScheduledProcedureStepStartTime' in sps:
        val = sps.ScheduledProcedureStepStartTime
        mwl_item['sps']['start_time'] = val
    if 'ScheduledProcedureStepID' in sps:
        val = sps.ScheduledProcedureStepID
        mwl_item['sps']['sps_id'] = val
    if 'ScheduledProcedureStepDescription' in sps:
        val = sps.ScheduledProcedureStepDescription
        mwl_item['sps']['sps_desc'] = val
    if 'ScheduledProcedureStepStatus' in sps:
        val = sps.ScheduledProcedureStepStatus
        mwl_item['sps']['status'] = val
    if 'RequestedContrastAgent' in sps:
        val = sps.RequestedContrastAgent
        mwl_item['sps']['contrast_agent'] = val
    if 'PreMedication' in sps:
        val = sps.PreMedication
        mwl_item['sps']['pre_meds'] = val
    if 'CommentsOnTheScheduledProcedureStep' in sps:
        val = sps.CommentsOnTheScheduledProcedureStep
        mwl_item['sps']['comments'] = val
    if 'ScheduledPerformingPhysicianName' in sps:
        if 'Alphabetic' in sps.ScheduledPerformingPhysicianName:
            val = sps.ScheduledPerformingPhysicianName['Alphabetic']
        else:
            val = sps.ScheduledPerformingPhysicianName
        names = parse_person_name(val)
        mwl_item['sps']['operator'] = names[0] + ' ' + names[1]
    if 'ScheduledProtocolCodeSequence' in sps:
        val = sps.ScheduledProtocolCodeSequence
        if 'CodeValue' in val:
            mwl_item['sps']['protocol_code'] = val.CodeValue
        if 'CodeMeaning' in val:
            mwl_item['sps']['protocol_code_meaning'] = val.CodeMeaning
        if 'CodingSchemeDesignator' in val:
            mwl_item['sps']['protocol_code_scheme_designator'] = val.CodingSchemeDesignator

def fill_proc_info(ds, mwl_item):
    mwl_item['proc_info'] = {
        'requested_proc_desc': '',
        'proc_id':'',
        'study_uid':'',
        'proc_priority': 'LOW',
        'request_reason': ''
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
    if 'RequestedProcedurePriority' in ds:
        val = ds.RequestedProcedurePriority
        mwl_item['proc_info']['proc_priority'] = val
    if 'ReasonForTheRequestedProcedure' in ds:
        val = ds.ReasonForTheRequestedProcedure
        mwl_item['proc_info']['request_reason'] = val
    if 'RequestedProcedureCodeSequence' in ds:
        val = ds.RequestedProcedureCodeSequence
        if 'CodeValue' in val:
            mwl_item['proc_info']['procedure_code'] = val.CodeValue
        if 'CodeMeaning' in val:
            mwl_item['proc_info']['procedure_code_meaning'] = val.CodeMeaning
        if 'CodingSchemeDesignator' in val:
            mwl_item['proc_info']['proc_scheme_designator'] = val.CodingSchemeDesignator


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
    print (str(json_obj))
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
