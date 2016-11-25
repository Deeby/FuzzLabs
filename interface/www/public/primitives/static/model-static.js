app.factory('StaticModel', [
    function() {
        function StaticModel(data) {
            _.assign(this, data);
        }

        StaticModel.prototype.sampleFunction = function () {
            return 'staticmodel';
        };

        StaticModel.build = function (data) {
            return new StaticModel(data);
        };
        return StaticModel;
    }
]);
