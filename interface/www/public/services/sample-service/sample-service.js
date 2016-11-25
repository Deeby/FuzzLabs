app.service('sampleService', [
    function() {
        this.sample = function(cb) {
            cb(true);
        };
    }
]);
