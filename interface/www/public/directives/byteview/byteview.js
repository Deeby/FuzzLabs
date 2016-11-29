function byteView(utilityService, selectionService, propertiesService) {
    return {
        restrict: 'E',
        scope: {
            value: '=',
            offset: '=',
            bgcolor: '='
        },
        link: function(scope, element, attrs) {

            scope.type = "raw_byte";
            scope.selected = false;

            scope.onSelectionChange = function(status) {
                start = status.start;
                end   = status.current_offset;
                if (start > end) {
                    start = status.current_offset;
                    end   = status.start;
                }
                if (scope.offset >= start && scope.offset <= end) {
                    scope.selected = true;
                } else {
                    scope.selected = false;
                }
            }

            scope.showProperties = function() {
                propertiesService.passItem(scope);
                selectionService.updateCurrentOffset(scope.offset);
            }

            scope.byteSelected = function() {
                if (selectionService.isSelectionActive()) {
                    selectionService.setEndOffset(scope.offset);
                } else {
                    selectionService.setStartOffset(scope.offset);
                }
            }

            scope.render = utilityService.toHex(scope.value, false);
            selectionService.addSelectionChangeObserver(scope.onSelectionChange);
        },
        controller: ['$scope', function($scope) {
        }],
        templateUrl: '/directives/byteview/byteview.html.tpl'
    };
};
