app.factory('PaddingModel', [
    function() {
        function PaddingModel(data) {
            _.assign(this, data);
        }

        PaddingModel.prototype.sampleFunction = function () {
            return 'paddingmodel';
        };

        PaddingModel.build = function (data) {
            return new PaddingModel(data);
        };
        return PaddingModel;
    }
]);
