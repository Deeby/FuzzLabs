app.factory('RandomModel', [
    function() {
        function RandomModel(data) {
            _.assign(this, data);
        }

        RandomModel.prototype.sampleFunction = function () {
            return 'randommodel';
        };

        RandomModel.build = function (data) {
            return new RandomModel(data);
        };
        return RandomModel;
    }
]);
