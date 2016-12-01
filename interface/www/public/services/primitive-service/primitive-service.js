primitiveService.$inject = [
    'utilityService'
]
app.factory('primitiveService', primitiveService);

var primitiveBaseBinary = function(name, value, fuzzable) {
    return {
        "name": name,
        "value": value,
        "fuzzable": fuzzable
    }
}

var primitiveBase = function(parent, id, type, primitive) {
    return {
        "primitive": type,
        "properties": primitive,
        "meta": {
            "id": id,
            "parent": parent
        }
    };
};

function primitiveService(utilityService) {
    var observers = [];
    this.data = [];

    var notifyObservers = function() {
        angular.forEach(observers, function(callback){
            callback();
        });
    }

    /* This function to merge binary primitives next to
       each other. This is because binary primitives form
       a pool of parseable data.
    */
    var mergeBinaryPrimitives = function() {
    }

    this.initRoot = function(value) {
        this.data.length = 0;
        var d = [];
        for (var i = 0; i < value.length; i++) {
            d.push(value[i]);
        }
        this.data.push(new primitiveBase(
            this.data,
            utilityService.uuid(),
            "binary",
            primitiveBaseBinary(
                "pool",
                d,
                0
            )
        ));
        notifyObservers();
    }

    this.registerObserver = function(callback) {
        observers.push(callback);
    }

    this.addPrimitive = function(parent, primitive) {
    }

    return this;
}
