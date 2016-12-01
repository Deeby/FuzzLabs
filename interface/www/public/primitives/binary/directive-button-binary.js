function buttonBinary(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('binary');
        }],
        templateUrl: '/primitives/binary/view-button-binary.html.tpl'
    };
};

