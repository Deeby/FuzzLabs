function buttonRandom(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('random');
        }],
        templateUrl: '/primitives/random/view-button-random.html.tpl'
    };
};

