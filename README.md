# Webmwl
This is a Web2Py module which provides Modality Worklist functionality in connection with dcm4chee-arc. It provides
functionalities of
- Maintaining Patient List (locally on Web2py)
- Maintaining list of stations (Modalities) (locally on Web2py)
- Maintaining list of Procedures (locally on Web2py)
- Managing (Create / update / Delete) of Modality Worklists on Dcm4chee-arc

## Python Dependencies
The following are the python modules which are required to be installed on the site-packages folder of Web2py.
- pydicom
- requests

When you install these 2 modules it would install other dependencies as well. 
Use the following pip command to install to a specific folder.
```
pip install -t <site-packages-folder> <package_name>
```
## Other Tool dependencies
This module requires dcm2xml tool from dcmtk (offis) to be present in the "modules" folder. This tool is used for xml conversion
of Completed MWL objects for non DICOM complying modalities.
The tool can be downloaded from
https://dicom.offis.de/dcmtk.php.en

## Setup
By default this module will try to communicate with dcm4che-arc on localhost port 8080. However this can be changed from the 
"ArcConfig" Menu item once the modules is loaded with Web2py.

## Non DICOM complying modalities
For non DICOM complying modalities, there is an option on the MWL list to "COMPLETE" the worklist item. If invoked it would create
a .dcm file as well as a .xml file in the "completed_items" folder under the webmwl folder structure.
