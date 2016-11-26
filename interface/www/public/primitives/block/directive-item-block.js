function itemBlock(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'AEC',
        scope: {
            value: '='
        },
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
        }],
        templateUrl: '/primitives/block/view-item-block.html.tpl'
    };
};

