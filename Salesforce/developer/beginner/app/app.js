var stateProv;
var app = angular.module('plunker', ['ui.router', 'ct.ui.router.extras']);

app.config(function ($stateProvider, $urlRouterProvider) {
  $stateProvider.state('root', {
    url: "/",
    template: "<div ui-view></div>"
  });
  //$urlRouterProvider.otherwise("/");
  stateProv = $stateProvider;

});

app.provider('routes', function () {
  function registerRoutes(states) {
    angular.forEach(states, function (stateObject) {
      stateProv.state(stateObject);
    });
  }

  this.$get = function ($http, storageService) {
    return {
      initilize: function () {
        return $http.get('states.json').then(function (response) {
          storageService.states = response.data.routes;
          registerRoutes(response.data.routes);
        }, function (error) {

        });
      }
    }
  };
});

app.service('storageService', function () {
  this.states = [];
})

app.controller('main', function ($scope, $http, storageService) {
  // $scope.$watch('storageService.states', function(newVal) {
  //   $scope.states = newVal;
  // });
  $http.get('states.json').then(function (response) {
    var rts = response.data.routes;
    var currentModule = null;
    var _modules = [], module;
    for (var i = 0, len = rts.length; i < len; i++) {
      if (currentModule !== rts[i].moduleName) {
        currentModule = rts[i].moduleName;
        module = {
          name: currentModule,
          isCollapsed: false,
          states: []
        };
        _modules.push(module);
      }
      module.states.push({
        url: rts[i].url,
        templateUrl: rts[i].templateUrl,
        name: rts[i].name
      });
    }
    $scope.modules = _modules;
  }, function (error) {

  });
});

app.directive('syntaxHighlighter', function () {
  return {
    restrict: 'A',
    link: function ($scope, el, attr, ctrl) {
      // fix code snippets
      $.each(el.find('pre'), function (index, item) {
        $(item).html($(item).html().replace(/<[^>]+>/gi, ''));
      });

      el.find('pre').addClass('brush: apex;');
      SyntaxHighlighter.config.clipboardSwf = "https://trailhead.salesforce.com/assets/clipboard-583bcb178f3e17f27a8042d7eea29f8c9c039b17aa3cbf8bdfa8442ab264191e.swf";
      SyntaxHighlighter.highlight();
    }
  };
});

app.run(["routes", function (routes, $state) {
  routes.initilize();
  console.info("$state:", $state);
}]);