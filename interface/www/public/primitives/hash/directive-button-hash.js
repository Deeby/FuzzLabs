function buttonHash(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
            propertiesService.showPrimitiveProperties('hash');
        }],
        templateUrl: '/primitives/hash/view-button-hash.html.tpl'
    };
};

