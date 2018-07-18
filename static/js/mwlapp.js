var mwlapp = angular.module('mwlapp', ['ui.bootstrap']);

mwlapp.config(function($interpolateProvider) {
    //allow Web2py views and Angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

mwlapp.controller('MwlListController', ['$scope','$http', function($scope, $http) {
  var vm = this
  $scope.selectedStatus = 'SCHEDULED'
  $scope.selectedDate = 'TODAY'
  $scope.fltr = {}
  $scope.fltr.selectedFilterDate = new Date()
  $scope.fltr.searchString = ''
  $scope.selectedModality = 'ALL'
  $scope.modalities = ["CR", "CT", "DX", "MR", "MG", "NM","US", "ES", "EPS","ECG","BMD","BI","PT","OPT", "OT", "RF", "XA"]
  $scope.format = 'dd-MMMM-yyyy'
  $scope.show_list = true
  $scope.show_edit = false
  $scope.loading = false
  $scope.popup1 = {
    opened: false
  }
  $scope.popup2 = {
    opened: false
  }
  $scope.dateOptions = {
    formatYear: 'yyyy',
    startingDay: 1,
    showWeeks: false
  }
  $scope.currentPage = 1
  $scope.pageSize = 10
  $scope.totalCount = 0
  $scope.pages = 1

  $scope.mwlItems = []

  $scope.selected_station = undefined
  $scope.selected_procedure = undefined
  $scope.selected_patient = undefined

  $scope.today = function () {
      var date = new Date()
      return date
      // date.setDate(date.getDate()-1)
      // return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2)
    }
  $scope.yesterday = function () {
      var date = new Date()
      date.setDate(date.getDate() - 1)
      return date
    }
  $scope.tomorrow = function () {
      var date = new Date()
      date.setDate(date.getDate() + 1)
      return date
      //return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2)
    }
  $scope.formatDate = function (date) {
    return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2)
  }
  $scope.formatDateDicom = function (date) {
    return date.getFullYear() + ('0' + (date.getMonth() + 1)).slice(-2) + ('0' + date.getDate()).slice(-2)
  }
  $scope.formatTimeDicom = function (date) {
    return  ('0' + (date.getHours())).slice(-2) + ('0' + date.getMinutes()).slice(-2) + ('0' + date.getSeconds()).slice(-2)
  }
  var getAge = function (dateString) {
      var today = new Date()
      var birthDate = new Date(dateString)
      var age = today.getFullYear() - birthDate.getFullYear()
      var m = today.getMonth() - birthDate.getMonth()
      if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--
      }
      if (age > 0) {
        return age + ' years'
      }
      return Math.abs(m) + ' months'
  }
  $scope.getStationDcmCompliance = function(mwl_item) {
    var item = mwl_item
    var qparams = {params: {'search_str': mwl_item['sps']['station_name']}}
    var promise = $http.get('get_stations', qparams)
    promise.then (function (response) {
      var matching_stations = response.data['result']
      for (i=0; i<matching_stations.length;i++) {
        if (matching_stations[i]['name'] === mwl_item['sps']['station_name']) {
          mwl_item['sps']['station_dicom_compliant'] = matching_stations[i]['DICOM_Compliant']
        }
      }
    })
    .catch( function(error) {
      console.log('Error ='+ error)
    })
  }
  $scope.loadMwlItems = function() {
    $scope.loading = true
    var qparams = {params: {'status': $scope.selectedStatus,
      'date': $scope.formatDate($scope.fltr.selectedFilterDate),
      'search': ($scope.fltr.searchString !== '') ? ($scope.fltr.searchString + '*') : '',
      'modality': $scope.selectedModality,
      'page': $scope.currentPage,
      'pageSize': $scope.pageSize}}

    var promise = $http.get('get_mwl',qparams)
    promise.then (function (response) {
      $scope.mwlItems.length = 0
      $scope.mwlItems.push.apply($scope.mwlItems,response.data['result']['items'])
      for (i=0; i< $scope.mwlItems.length; i++) {
        $scope.mwlItems[i]['patient']['age'] = getAge($scope.mwlItems[i]['patient']['dob'])
        $scope.mwlItems[i]['sps']['station_dicom_compliant'] = false
        $scope.getStationDcmCompliance($scope.mwlItems[i])
      }
      $scope.totalCount = response.data['result']['count']
      $scope.pages = Math.floor($scope.totalCount / $scope.pageSize)
      if ($scope.totalCount % $scope.pageSize > 0) {
        $scope.pages = $scope.pages + 1
      }
      // console.log(data)
      $scope.loading = false
    })
    .catch( function(error) {
      $scope.loading = false
      console.log('Error ='+ error)
    })
  }
  $scope.getPages = function () {
    return new Array($scope.pages)
  }
  $scope.selectModality = function (modality) {
    $scope.selectedModality = modality
    $scope.loadMwlItems()
  }
  $scope.selectYesterday = function () {
    $scope.selectedDate = 'YESTERDAY'
    $scope.fltr.selectedFilterDate = $scope.yesterday()
    $scope.loadMwlItems()
  }
  $scope.selectToday = function () {
    $scope.selectedDate = 'TODAY'
    $scope.fltr.selectedFilterDate = $scope.today()
    $scope.loadMwlItems()
  }
  $scope.selectTomorrow = function () {
    $scope.selectedDate = 'TOMORROW'
    $scope.fltr.selectedFilterDate = $scope.tomorrow()
    $scope.loadMwlItems()
  }
  $scope.selectADate = function () {
    $scope.selectedDate = 'DATE'
  }
  $scope.selectScheduled = function () {
    $scope.selectedStatus = 'SCHEDULED'
    $scope.loadMwlItems()
  }
  $scope.selectInProgress = function () {
    $scope.selectedStatus = 'IN PROGRESS'
    $scope.loadMwlItems()
  }
  $scope.selectCompleted = function () {
    $scope.selectedStatus = 'COMPLETED'
    $scope.loadMwlItems()
  }
  $scope.open1 = function() {
    $scope.popup1.opened = true;
  }
  $scope.delete_wl = function(index) {
    var studyUid = $scope.mwlItems[index]['proc_info']['study_uid']
    var spsId = $scope.mwlItems[index]['sps']['sps_id']
    swal({
      title: "Are you sure?",
      text: "The selected worklist item will be deleted !",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then((willDelete) => {
      if (willDelete) {
          var promise = $http.post('del_mwl', params={'studyUid':studyUid,'spsId':spsId})
          promise.then( function(data) {
            swal({
              title: "Success",
              text: "The selected item has been deleted",
              icon: "success",
              button: "OK",
            })
            $scope.loadMwlItems()
          })
      }
    })
  }
  $scope.complete_wl = function(index) {
    var worklist = $scope.mwlItems[index]
    swal({
      title: "Are you sure?",
      text: "The selected worklist item will be marked as Completed !",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then((willComplete) => {
      if (willComplete) {
          worklist['sps']['status'] = 'COMPLETED'
          var promise = $http.post('complete_mwl', params=worklist)
          promise.then( function(data) {
            swal({
              title: "Success",
              text: "The selected item has been marked as complete",
              icon: "success",
              button: "OK",
            })
            $scope.loadMwlItems()
          })
      }
    })
  }
  $scope.convert_dicom_date_to_date = function(dtString) {
    var year = dtString.substring(0,4)
    var month = dtString.substring(4,6)
    var day = dtString.substring(6,8)
    return new Date(year+'-'+month+'-'+day)
  }
  $scope.editwl = function (index) {
    $scope.wl_to_edit = $scope.mwlItems[index]
    $scope.wl_to_edit['patient']['dob'] = new Date($scope.wl_to_edit['patient']['dob'])
    $scope.wl_to_edit['sps']['start_date'] = new Date($scope.wl_to_edit['sps']['start_date'])
    var st_time = new Date()
    if ($scope.wl_to_edit['sps']['start_time'] !== '') {
      var tmString = $scope.wl_to_edit['sps']['start_time']
      st_time.setHours(parseInt(tmString.substring(0,2)))
      st_time.setMinutes(parseInt(tmString.substring(2,4)))
    }
    $scope.wl_to_edit['sps']['start_time'] = st_time
    $scope.show_list = false
    $scope.show_edit = true
    $scope.title = 'Edit'
    $scope.action = 'Change'
    $scope.save_requested = false
  }
  $scope.init_validations = function () {
    $scope.patient_valid = false
    $scope.isr_valid = false
    $scope.schedule_valid = false
    $scope.procedure_valid = false
  }
  $scope.addwl = function () {
    // $scope.wl_to_edit = $scope.mwlItems[index]
    $scope.initwl()
    $scope.show_list = false
    $scope.show_edit = true
    $scope.title = 'Add'
    $scope.action = 'Select'
    $scope.save_requested = false
  }
  $scope.initwl = function () {
    $scope.wl_to_edit = {}
    $scope.wl_to_edit['patient'] = {
      'last_name': '',
      'first_name': '',
      'gender': 'Male',
      'dob': '',
      'weight': '',
      'patient_id': '',
      'patient_size':'',
      'med_alerts':'',
      'allergies': ''
      }
    $scope.wl_to_edit['isr'] = {
          'accession_number': '',
          'requesting_physician': '',
          'referring_physician': ''
      }
    $scope.wl_to_edit['sps'] = {
          'modality': '',
          'station_aet': '',
          'station_name': '',
          'start_date':new Date(),
          'start_time': new Date(),
          'sps_id': '',
          'sps_desc':'',
          'status':'SCHEDULED',
          'contrast_agent': '',
          'pre_meds':'',
          'operator':'',
          'comments':'',
          'protocol_code': '',
          'protocol_code_meaning': '',
          'protocol_code_scheme_designator': ''
      }
    $scope.wl_to_edit['proc_info'] = {
          'requested_proc_desc': '',
          'proc_id':'',
          'study_uid':'',
          'proc_priority': 'ROUTINE',
          'request_reason': '',
          'procedure_code': '',
          'procedure_code_meaning': '',
          'proc_scheme_designator':''
      }
  }
  // Add Edit MwlListController
  $scope.title = ''
  $scope.action = ''
  $scope.procSearch=''
  $scope.stationSearch=''
  $scope.patientSearch=''
  $scope.priorities = ['STAT','ROUTINE', 'LOW', 'HIGH', 'MEDIUM']
  $scope.open2 = function() {
    $scope.popup2.opened = true;
  }
  $scope.cancel = function() {
    $scope.show_list = true
    $scope.show_edit = false
    $scope.loadMwlItems()
  }
  $scope.checkIsrFormValid = function () {
    valid = vm.mwlForm.accession_number.$valid &&
      vm.mwlForm.requesting_physician.$valid &&
      vm.mwlForm.referring_physician.$valid
    if (!valid) {
      $('#isrForm').collapse('show')
    }
    return valid
  }
  $scope.checkScheduleFormValid = function () {
    valid = vm.mwlForm.stationname.$valid &&
      vm.mwlForm.stationaet.$valid &&
      vm.mwlForm.modality.$valid
    if (!valid) {
      $('#scheduleForm').collapse('show')
    }
    return valid
  }
  $scope.checkRequestFormValid = function () {
    valid = vm.mwlForm.procedure.$valid
    if (!valid) {
      $('#procedureForm').collapse('show')
    }
    return valid
  }
  $scope.checkPatientFormValid = function () {
    valid = vm.mwlForm.first_name.$valid &&
      vm.mwlForm.last_name.$valid &&
      vm.mwlForm.patient_id.$valid &&
      vm.mwlForm.dob.$valid
    if (!valid) {
      $('#patientForm').collapse('show')
    }
    return valid
  }
  $scope.validateForm = function() {
    return $scope.checkPatientFormValid() &&
      $scope.checkIsrFormValid() &&
      $scope.checkScheduleFormValid() &&
      $scope.checkRequestFormValid()
  }
  $scope.save = function () {
    $scope.save_requested = true
    if (!$scope.validateForm()) {
      return
    }
    // Fix dates
    $scope.wl_to_edit['sps']['start_date'] = $scope.formatDateDicom($scope.wl_to_edit['sps']['start_date'])
    $scope.wl_to_edit['patient']['dob'] = $scope.formatDateDicom($scope.wl_to_edit['patient']['dob'])
    $scope.wl_to_edit['sps']['start_time'] = $scope.formatTimeDicom($scope.wl_to_edit['sps']['start_time'])
    var promise = $http.post('save_mwl',$scope.wl_to_edit)
    promise.then ( function(result) {
      console.log('Saved Successfully')
      $scope.cancel()
      swal({
        title: "Success",
        text: "Worklist item has been saved successfully",
        icon: "success",
        button: "OK",
      })
    })
    .catch ( function(error) {
      console.log('Error in Saving MWL ' + error)
      $scope.cancel()
    })
  }

  $scope.loadStations = function(search_str) {
    $scope.stations = []
    var qparams = {params: {'search_str': search_str}}
    var promise = $http.get('get_stations', qparams)
    promise.then (function (response) {
      $scope.stations.length = 0
      $scope.stations.push.apply($scope.stations,response.data['result'])
      return $scope.stations
    })
    .catch( function(error) {
      console.log('Error ='+ error)
    })
  }
  $scope.loadProcedures = function(search_str) {
    $scope.procedures = []
    var qparams = {params: {'search_str': search_str}}
    var promise = $http.get('get_procedures', qparams)
    promise.then (function (response) {
      $scope.procedures.length = 0
      $scope.procedures.push.apply($scope.procedures,response.data['result'])
      return $scope.procedures
    })
    .catch( function(error) {
      console.log('Error ='+ error)
    })
  }
  $scope.loadPatients = function(search_str) {
    $scope.patients = []
    var qparams = {params: {'search_str': search_str}}
    var promise = $http.get('get_patients',qparams)
    promise.then (function (response) {
      $scope.patients.length = 0
      $scope.patients.push.apply($scope.patients,response.data['result'])
      return $scope.patients
    })
    .catch( function(error) {
      console.log('Error ='+ error)
    })
  }

  $scope.$watch(function(scope) { return scope.procSearch },
              function() {
                if ($scope.procSearch !== '') {
                  $scope.loadProcedures($scope.procSearch)
                }
              })
  $scope.$watch(function(scope) { return scope.stationSearch },
                function() {
                  if ($scope.stationSearch !== '') {
                      $scope.loadStations($scope.stationSearch)
                  }
                })
  $scope.$watch(function(scope) { return scope.patientSearch },
                function() {
                  if ($scope.patientSearch !== '') {
                    $scope.loadPatients($scope.patientSearch)
                  }
                })
  $scope.$watch(function(scope) { return scope.popup1.opened },
                function() {
                  if(! $scope.popup1.opened && $scope.selectedDate === 'DATE') {
                    $scope.loadMwlItems()
                  }
                })
  $scope.procedureSelected = function (index) {
    var proc_info = $scope.wl_to_edit['proc_info']
    proc_info['requested_proc_desc'] = $scope.procedures[index].procedure_description
    proc_info['proc_id'] = $scope.procedures[index].procedure_id
    proc_info['procedure_code'] = $scope.procedures[index].procedure_code
    proc_info['procedure_code_meaning'] = $scope.procedures[index].procedure_code_meaning
    proc_info['proc_scheme_designator'] = $scope.procedures[index].procedure_code_scheme_designator
    // Fill sps protocol
    var sps = $scope.wl_to_edit['sps']
    sps['protocol_code'] = $scope.procedures[index].protocol_code
    sps['protocol_code_meaning'] = $scope.procedures[index].protocol_code_meaning
    sps['protocol_code_scheme_designator'] = $scope.procedures[index].protocol_code_scheme_designator
    $('#procedureModal').modal('hide')

  }
  $scope.stationSelected = function (index) {
    var sps_info = $scope.wl_to_edit['sps']
    sps_info['station_aet'] = $scope.stations[index].AE_title
    sps_info['station_name'] = $scope.stations[index].name
    sps_info['modality'] = $scope.stations[index].modality
    $('#stationModal').modal('hide')
    $('#scheduleForm').collapse('hide')
    setTimeout(function() {
      $('#procedureForm').collapse('show')
    },500)
  }
  $scope.patientSelected = function (index) {
    var patient_info = $scope.wl_to_edit['patient']
    patient_info['last_name'] = $scope.patients[index].last_name
    patient_info['first_name'] = $scope.patients[index].first_name
    patient_info['patient_id'] = $scope.patients[index].patient_id
    patient_info['gender'] = $scope.patients[index].gender
    patient_info['dob'] = new Date($scope.patients[index].birth_date)
    patient_info['weight'] = $scope.patients[index].weight
    patient_info['patient_size'] = $scope.patients[index].patient_size
    $('#patientModal').modal('hide')
    $('#patientForm').collapse('hide')
    //$('#isrForm').collapse({'toggle':true, 'parent':'#accordion'})
    setTimeout(function() {
      $('#isrForm').collapse('show')
    },500)
  }
  // pagination
  $scope.pageChanged = function (index) {
    $scope.currentPage = index
    $scope.loadMwlItems()
  }
  $scope.prevPage = function () {
    $scope.pageChanged($scope.currentPage -1)
  }
  $scope.nextPage = function () {
    $scope.pageChanged($scope.currentPage + 1)
  }
  // Initial load
  $scope.loadMwlItems()
  //$scope.loadStations()
  //$scope.loadProcedures()
  //$scope.loadPatients()
}])
