function buttonIncrement(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('increment');
        }],
        templateUrl: '/primitives/increment/view-button-increment.html.tpl'
    };
};

