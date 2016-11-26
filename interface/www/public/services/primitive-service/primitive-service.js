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
            // Clear selection service
            this.data.length = 0;
            for (var i = 0; i < value.length; i++) {
                this.data.push(value[i]);
            }
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
