var primitiveBase = function(parent, primitive, name, fuzzable, value) {
    return {
        "primitive": primitive,
        "properties": {
            "name": name,
            "value": value,
            "fuzzable": fuzzable,
        },
        "meta": {
            "properties": {
                "parent": parent
            },
            "getParent": function() {
                return this.properties.parent;
            }
        }
    };
};

app.factory('primitiveService', [
    function() {
        var observers = [];
        this.data = [];

        var notifyObservers = function() {
            angular.forEach(observers, function(callback){
                callback();
            });
        }

        this.initRoot = function(value) {
            this.data.length = 0;
            var d = [];
            for (var i = 0; i < value.length; i++) {
                d.push(value[i]);
            }
            this.data.push(new primitiveBase(this.data, "binary", "data", 0, d));
            notifyObservers();
        }

        this.registerObserver = function(callback) {
            observers.push(callback);
        }

        this.addPrimitive = function(parent, primitive) {
        }

        return this;
    }
]);
