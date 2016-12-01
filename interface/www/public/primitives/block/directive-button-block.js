function buttonBlock(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('block');
        }],
        templateUrl: '/primitives/block/view-button-block.html.tpl'
    };
};

