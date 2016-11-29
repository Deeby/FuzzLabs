function item<%= primitiveCapName %>(utilityService, selectionService, propertiesService, primitiveService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
        }],
        templateUrl: '/primitives/<%= primitiveName %>/view-button-<%= primitiveName %>.html.tpl'
    };
};

