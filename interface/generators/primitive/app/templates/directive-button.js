function button<%= primitiveCapName %>(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('<%= primitiveName %>');
        }],
        templateUrl: '/primitives/<%= primitiveName %>/view-button-<%= primitiveName %>.html.tpl'
    };
};

