function buttonDelimiter(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('delimiter');
        }],
        templateUrl: '/primitives/delimiter/view-button-delimiter.html.tpl'
    };
};

