app.factory('NumericModel', [
    function() {
        function NumericModel(data) {
            _.assign(this, data);
        }

        NumericModel.prototype.sampleFunction = function () {
            return 'numericmodel';
        };

        NumericModel.build = function (data) {
            return new NumericModel(data);
        };
        return NumericModel;
    }
]);
