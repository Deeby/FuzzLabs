app.factory('DelimiterModel', [
    function() {
        function DelimiterModel(data) {
            _.assign(this, data);
        }

        DelimiterModel.prototype.sampleFunction = function () {
            return 'delimitermodel';
        };

        DelimiterModel.build = function (data) {
            return new DelimiterModel(data);
        };
        return DelimiterModel;
    }
]);
