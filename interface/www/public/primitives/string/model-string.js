app.factory('StringModel', [
    function() {
        function StringModel(data) {
            _.assign(this, data);
        }

        StringModel.prototype.sampleFunction = function () {
            return 'stringmodel';
        };

        StringModel.build = function (data) {
            return new StringModel(data);
        };
        return StringModel;
    }
]);
