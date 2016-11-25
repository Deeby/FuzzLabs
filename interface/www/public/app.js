var dependencies = ['ngRoute', 'ngMaterial', 'ngFileUpload'];
var routes = [];
var app = angular.module('testApp', dependencies);

app.config(['$routeProvider',
    function($routeProvider) {
        _.forEach(routes, function(route) {
            var path = route.path || "/"+route.module;
            var templateUrl = route.templateUrl || "/modules/"+route.module+"/"+route.module+".html.tpl";
            var controller = route.controller || route.module+"Controller";
            var route = {
                'templateUrl': templateUrl,
                'controller': controller
            }
            $routeProvider.when(path, route)
        });
        $routeProvider.otherwise({redirectTo: '/sample'});
    }
]);

// routes
dependencies.push('sample');
routes.push({'module': 'sample'});
