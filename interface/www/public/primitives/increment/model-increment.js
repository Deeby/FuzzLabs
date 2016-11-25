app.factory('IncrementModel', [
    function() {
        function IncrementModel(data) {
            _.assign(this, data);
        }

        IncrementModel.prototype.sampleFunction = function () {
            return 'incrementmodel';
        };

        IncrementModel.build = function (data) {
            return new IncrementModel(data);
        };
        return IncrementModel;
    }
]);
