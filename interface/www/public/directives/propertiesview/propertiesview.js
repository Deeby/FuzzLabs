function propertiesView(propertiesService) {
    return {
        restrict: 'E',
        scope: {},
        controller: ['$scope', function($scope) {

            $scope.showSelection = false;
            $scope.unit = {
                "name": "",
                "description": ""
            };

            var updateInterface = function() {
                var selection = propertiesService.getSelection();
                $scope.primitive = selection.primitive;
                $scope.item_offset = selection.item_offset.value;
                $scope.item_offset_hex = selection.item_offset.hex;
                $scope.item_value = selection.item_value.value;
                $scope.item_value_hex = selection.item_value.hex;
                $scope.item_value_ascii = selection.item_value.ascii;
                $scope.showSelection = true;
            }

            propertiesService.registerObserver(updateInterface);
        }],
        templateUrl: '/directives/propertiesview/propertiesview.html.tpl'
    };
}

