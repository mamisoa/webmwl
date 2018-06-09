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
  $scope.dateOptions = {
    formatYear: 'yyyy',
    startingDay: 1,
    showWeeks: false
  }
  $scope.currentPage = 1
  $scope.pageSize = 10

  $scope.mwlItems = []
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
    // $scope.show_list = false
    // $scope.show_edit = true
  }
  // Initial load
  $scope.loadMwlItems()
}])
