app.factory('BinaryModel', [
    function() {
        function BinaryModel(data) {
            _.assign(this, data);
        }

        BinaryModel.prototype.sampleFunction = function () {
            return 'binarymodel';
        };

        BinaryModel.build = function (data) {
            return new BinaryModel(data);
        };
        return BinaryModel;
    }
]);
