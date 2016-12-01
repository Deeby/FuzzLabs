function buttonNumeric(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('numeric');
        }],
        templateUrl: '/primitives/numeric/view-button-numeric.html.tpl'
    };
};

