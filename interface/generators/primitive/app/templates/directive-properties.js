function properties<%= primitiveCapName %>(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {

        }],
        templateUrl: '/primitives/<%= primitiveName %>/view-properties-<%= primitiveName %>.html.tpl'
    };
};

