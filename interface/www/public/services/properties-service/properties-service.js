propertiesService.$inject = [
    'utilityService',
    'selectionService'
]
app.factory('propertiesService', propertiesService);

function propertiesService(utilityService, selectionService) {
    var observers = [];
    var data = {
        "selection": {
            "primitive": "",
            "item_type": "",
            "item_offset": {
                "value": 0,
                "hex": ""
            },
            "item_value": {
                "value": 0,
                "hex": "",
                "ascii": ""
            }
        }
    };

    this.showPrimitiveProperties = function(type) {
    }

    var notifyObservers = function() {
        angular.forEach(observers, function(callback) {
            callback();
        });
    }

    this.registerObserver = function(callback) {
        observers.push(callback);
    }

    this.getSelection = function() {
        return data.selection;
    }

    this.passItem = function(value) {
        data.selection.item_type         = "Raw byte";
        data.selection.primitive         = value.parent;
        data.selection.item_offset.value = value.offset;
        data.selection.item_value.value  = value.value;
        data.selection.item_offset.hex   = utilityService.toHex(value.offset, true);
        data.selection.item_value.hex    = utilityService.toHex(value.value, true);
        data.selection.item_value.ascii  = utilityService.toAscii(value.value);
        notifyObservers();
    };
    return this;
}
