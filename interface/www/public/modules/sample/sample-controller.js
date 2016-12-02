sampleController.$inject = ['$scope', 
                            'utilityService', 
                            'selectionService', 
                            'propertiesService', 
                            'primitiveService'];
var designer = angular.module('sample');
designer.controller('sampleController', sampleController);
designer.directive('propertiesView', ['propertiesService', propertiesView]);
designer.directive('byteView', ['utilityService', 'selectionService', 'propertiesService', byteView]);
designer.directive('buttonBlock', ['utilityService', 'selectionService', 'propertiesService', buttonBlock]);
designer.directive('buttonStatic', ['utilityService', 'selectionService', 'propertiesService', buttonStatic]);
designer.directive('buttonString', ['utilityService', 'selectionService', 'propertiesService', buttonString]);
designer.directive('buttonDelimiter', ['utilityService', 'selectionService', 'propertiesService', buttonDelimiter]);
designer.directive('buttonHash', ['utilityService', 'selectionService', 'propertiesService', buttonHash]);
designer.directive('buttonIncrement', ['utilityService', 'selectionService', 'propertiesService', buttonIncrement]);
designer.directive('buttonPadding', ['utilityService', 'selectionService', 'propertiesService', buttonPadding]);
designer.directive('buttonRandom', ['utilityService', 'selectionService', 'propertiesService', buttonRandom]);
designer.directive('buttonSizer', ['utilityService', 'selectionService', 'propertiesService', buttonSizer]);

// ----------------------- Binary Primitive ------------------------

designer.directive('buttonBinary', [
    'utilityService', 
    'selectionService', 
    'propertiesService', 
    buttonBinary
]);
designer.directive('primitiveBinary', [
    'utilityService', 
    'selectionService', 
    'propertiesService', 
    'primitiveService', 
    itemBinary
]);
designer.directive('primitiveBinaryProperties', [
    'utilityService', 
    'selectionService',
    'propertiesService',
    'primitiveService',
    propertiesBinary
]);

// ---------------------- Numeric Primitive ------------------------

designer.directive('buttonNumeric', [
    'utilityService',
    'selectionService',
    'propertiesService',
    buttonNumeric
]);
designer.directive('primitiveNumeric', [
    'utilityService',
    'selectionService',
    'propertiesService',
    'primitiveService',
    itemNumeric
]);
designer.directive('primitiveNumericProperties', [
    'utilityService',
    'selectionService',
    'propertiesService',
    'primitiveService',
    propertiesNumeric
]);

function sampleController($scope, utilityService, selectionService, propertiesService, primitiveService) {
    $scope.data = primitiveService.data;
    $scope.opened = false;
    $scope.reader = new FileReader();

    $scope.onPrimitiveServiceChange = function() {
        // TODO: data changed
    }

    /* Converts the ArrayBuffer into an Array once
     * file data is available.
     */

    $scope.onFileRead = function(evt) {
        d = Array.from(new Uint8Array(
            evt.target.result, 
            0, 
            evt.target.result.byteLength
        ));
        selectionService.resetSelection();
        primitiveService.initRoot(d);
        $scope.opened = true;
        $scope.$apply();
    };

    /* Gets called when a file dropped onto the area.
     * The contents of the file is being read as an
     * Array Buffer.
     */

    $scope.fileOpen = function(files) {
        $scope.reader.onloadend = $scope.onFileRead;
        $scope.reader.readAsArrayBuffer(files[0]);
    };

    $scope.close = function() {
        $scope.opened = false;
        selectionService.resetSelection();
        primitiveService.initRoot([]);
    }

    primitiveService.registerObserver($scope.onPrimitiveServiceChange);

}
