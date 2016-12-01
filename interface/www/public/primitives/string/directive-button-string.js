function buttonString(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('string');
        }],
        templateUrl: '/primitives/string/view-button-string.html.tpl'
    };
};

