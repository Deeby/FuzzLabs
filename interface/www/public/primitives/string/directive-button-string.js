function buttonString(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {

            $scope.createPrimitive = function(type) {
                propertiesService.showPrimitiveProperties(type);
            }

        }],
        templateUrl: '/primitives/string/view-button-string.html.tpl'
    };
};

