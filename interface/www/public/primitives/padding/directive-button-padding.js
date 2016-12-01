function buttonPadding(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('padding');
        }],
        templateUrl: '/primitives/padding/view-button-padding.html.tpl'
    };
};

