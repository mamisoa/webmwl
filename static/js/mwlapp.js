var mwlapp = angular.module('mwlapp', ['ui.bootstrap']);

mwlapp.config(function($interpolateProvider) {
    //allow Web2py views and Angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

mwlapp.controller('MwlListController', ['$scope','$http', function($scope, $http) {
  $scope.selectedStatus = 'SCHEDULED'
  $scope.selectedDate = 'TODAY'
  $scope.searchString = ''
  $scope.selectedFilterDate = new Date()
  $scope.format = 'dd-MMMM-yyyy'
  $scope.searchString = ''
  $scope.show_list = true
  $scope.show_edit = false
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
  $scope.loadMwlItems = function() {
    var qparams = {params: {'status': $scope.selectedStatus,
      'date': $scope.formatDate($scope.selectedFilterDate),
      'page': $scope.currentPage,
      'pageSize': $scope.pageSize}}
    if ($scope.searchString !== '') {
      qparams.params['search'] = $scope.searchString
    }
    var promise = $http.get('get_mwl',qparams)
    promise.then (function (response) {
      $scope.mwlItems.length = 0
      $scope.mwlItems.push.apply($scope.mwlItems,response.data['result'])
      for (i=0; i< $scope.mwlItems.length; i++) {
        $scope.mwlItems[i]['patient']['age'] = getAge($scope.mwlItems[i]['patient']['dob'])
      }
      console.log(data)
    })
    .catch( function(error) {
      console.log('Error ='+ error)
    })
  }
  $scope.selectYesterday = function () {
    $scope.selectedDate = 'YESTERDAY'
    $scope.selectedFilterDate = $scope.yesterday()
  }
  $scope.selectToday = function () {
    $scope.selectedDate = 'TODAY'
    $scope.selectedFilterDate = $scope.today()
  }
  $scope.selectTomorrow = function () {
    $scope.selectedDate = 'TOMORROW'
    $scope.selectedFilterDate = $scope.tomorrow()
  }
  $scope.selectADate = function () {
    $scope.selectedDate = 'DATE'
  }
  $scope.selectScheduled = function () {
    $scope.selectedStatus = 'SCHEDULED'
  }
  $scope.selectInProgress = function () {
    $scope.selectedStatus = 'IN PROGRESS'
  }
  $scope.selectCompleted = function () {
    $scope.selectedStatus = 'COMPLETED'
  }
  $scope.open1 = function() {
    $scope.popup1.opened = true;
  }
  $scope.editwl = function (index) {
    $scope.wl_to_edit = $scope.mwlItems[index]
    $scope.show_list = false
    $scope.show_edit = true
    $scope.title = 'Edit'
    $scope.action = 'Change'
  }
  $scope.addwl = function () {
    // $scope.wl_to_edit = $scope.mwlItems[index]
    $scope.initwl()
    $scope.show_list = false
    $scope.show_edit = true
    $scope.title = 'Add'
    $scope.action = 'Select'
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
      'patient_size':''
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
          'sps_id': '',
          'sps_desc':'',
          'status':'SCHEDULED'
      }
    $scope.wl_to_edit['proc_info'] = {
          'requested_proc_desc': '',
          'proc_id':'',
          'study_uid':''
      }
  }
  // Add Edit MwlListController
  $scope.title = ''
  $scope.action = ''
  $scope.procSearch=''
  $scope.stationSearch=''
  $scope.patientSearch=''
  $scope.open2 = function() {
    $scope.popup2.opened = true;
  }
  $scope.cancel = function() {
    $scope.show_list = true
    $scope.show_edit = false
    $scope.loadMwlItems()
  }
  $scope.save = function () {
    var promise = $http.post('save_mwl',$scope.wl_to_edit)
    promise.then ( function(result) {
      console.log('Saved Successfully')
      $scope.cancel()
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
  $scope.procedureSelected = function (index) {
    var proc_info = $scope.wl_to_edit['proc_info']
    proc_info['requested_proc_desc'] = $scope.procedures[index].procedure_description
    proc_info['proc_id'] = $scope.procedures[index].procedure_id
    $('#procedureModal').modal('hide')
  }
  $scope.stationSelected = function (index) {
    var sps_info = $scope.wl_to_edit['sps']
    sps_info['station_aet'] = $scope.stations[index].AE_title
    sps_info['station_name'] = $scope.stations[index].name
    sps_info['modality'] = $scope.stations[index].modality
    $('#stationModal').modal('hide')
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
  }
  // Initial load
  $scope.loadMwlItems()
  //$scope.loadStations()
  //$scope.loadProcedures()
  //$scope.loadPatients()
}])
