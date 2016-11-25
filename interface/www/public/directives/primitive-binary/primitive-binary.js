function primitiveBinary(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        scope: {
            value: '='
        },
        link: function(scope, element, attrs) {
            scope.setActivePrimitive = function() {
                selectionService.setActivePrimitive(scope.name, scope.value);
            }
        },
        controller: ['$scope', function($scope) {
        }],
        templateUrl: '/directives/primitive-binary/primitive-binary.html.tpl'
    };
};
