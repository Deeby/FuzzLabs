function buttonRandom(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {

            $scope.createPrimitive = function(type) {
                propertiesService.showPrimitiveProperties(type);
            }

        }],
        templateUrl: '/primitives/random/view-button-random.html.tpl'
    };
};

