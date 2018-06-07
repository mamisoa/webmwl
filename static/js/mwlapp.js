var mwlapp = angular.module('mwlapp', []);

mwlapp.config(function($interpolateProvider) {
    //allow Web2py views and Angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

mwlapp.controller('MwlListController', ['$scope','$http', function($scope, $http) {
  $scope.mwlItems = [
    {patient_name: 'John Doe',age:'45 years',gender:'Male',scheduled_date:'2018-05-18', modality:'DX', status:'SCHEDULED', requestedProcedureDesc:'Chest PA'},
    {patient_name: 'John Doe',age:'45 years',gender:'Male',scheduled_date:'2018-05-18', modality:'DX', status:'SCHEDULED', requestedProcedureDesc:'Chest PA'},
    {patient_name: 'John Doe',age:'45 years',gender:'Male',scheduled_date:'2018-05-18', modality:'DX', status:'SCHEDULED', requestedProcedureDesc:'Chest PA'},
    {patient_name: 'John Doe',age:'45 years',gender:'Male',scheduled_date:'2018-05-18', modality:'DX', status:'SCHEDULED', requestedProcedureDesc:'Chest PA'},
    {patient_name: 'John Doe',age:'45 years',gender:'Male',scheduled_date:'2018-05-18', modality:'DX', status:'SCHEDULED', requestedProcedureDesc:'Chest PA'}
  ]
  $scope.loadMwlItems = function() {

  }
  // Initial load
  $scpe.loadMwlItems()
}])
