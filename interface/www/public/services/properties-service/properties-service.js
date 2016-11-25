app.factory('propertiesService', ['utilityService',
    function(utilityService) {
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
        var observers = [];

        var notifyObservers = function() {
            angular.forEach(observers, function(callback){
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
            if (value.type == "raw_byte") {
                data.selection.item_type         = "Raw byte";
                data.selection.item_offset.value = value.offset;
                data.selection.item_value.value  = value.value;
                data.selection.item_offset.hex   = utilityService.toHex(value.offset, true);
                data.selection.item_value.hex    = utilityService.toHex(value.value, true);
                data.selection.item_value.ascii  = utilityService.toAscii(value.value);
            }
            notifyObservers();
        };
        return this;
    }
]);
