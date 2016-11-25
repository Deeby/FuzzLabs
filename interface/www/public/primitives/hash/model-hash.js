app.factory('HashModel', [
    function() {
        function HashModel(data) {
            _.assign(this, data);
        }

        HashModel.prototype.sampleFunction = function () {
            return 'hashmodel';
        };

        HashModel.build = function (data) {
            return new HashModel(data);
        };
        return HashModel;
    }
]);
