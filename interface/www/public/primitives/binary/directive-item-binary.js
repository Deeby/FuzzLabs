function itemBinary(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'AEC',
        scope: {
            value: '='
        },
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
        }],
        templateUrl: '/primitives/binary/view-item-binary.html.tpl'
    };
};

