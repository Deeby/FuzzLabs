function itemStatic(utilityService, selectionService, propertiesService, primitiveService) {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {
        }],
        templateUrl: '/primitives/static/view-button-static.html.tpl'
    };
};

