function itemBlock(utilityService, selectionService, propertiesService, primitiveService) {
    return {
        restrict: 'E',
        scope: {
            value: '='
        },
        link: function(scope, element, attrs) {
        },
        controller: ['$scope', function($scope) {

            $scope.showPrimitiveProperties = function() {
            }

            $scope.showModifyPrimitiveProperties = function() {
            }

        }],
        templateUrl: '/primitives/block/view-item-block.html.tpl'
    };
};

