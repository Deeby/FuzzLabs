app.service('<%= serviceName %>', [
    function() {
        this.sample = function(cb) {
            cb(true);
        };
    }
]);
