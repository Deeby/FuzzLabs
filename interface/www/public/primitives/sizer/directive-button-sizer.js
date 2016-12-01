function buttonSizer(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('sizer');
        }],
        templateUrl: '/primitives/sizer/view-button-sizer.html.tpl'
    };
};

