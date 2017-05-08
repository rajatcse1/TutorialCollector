Number.prototype.pad = function (n) {
  return new Array(n).join('0').slice((n || 2) * -1) + this;
};

function pad(str, max) {
  str = str.toString();
  return str.length < max ? pad("0" + str, max) : str;
}

var app = angular.module('plunker', ["ngRoute"]);

app.run(function ($location, $interval) {
  //return;
  // var count = 1, total = 601;
  // $interval(function () {
  //   if (count > total) {
  //     count = total;
  //   }
  //   $location.path('/Q' + pad(count, 4).toString());
  //   count = count + 1;
  // }, 1000)
});

app.controller('MainCtrl', function ($scope, $location) {
  //$scope.question = 1;
  $scope.onClick = function(question){
    $location.path('/Q' + pad(question, 4).toString());
  };
});

app.controller('routeCtrl', function ($scope) {


});
app.config(['$routeProvider', function ($routeProvider) {
  var count = 1, total = 601;
  while (count <= total) {
    var question = pad(count, 4).toString();
    $routeProvider.when('/Q' + question, {
      templateUrl: './pages/Q' + question + '.html',
      controller: 'routeCtrl'
    });
    count = count + 1;
  }

}]);