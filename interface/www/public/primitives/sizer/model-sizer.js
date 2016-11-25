app.factory('SizerModel', [
    function() {
        function SizerModel(data) {
            _.assign(this, data);
        }

        SizerModel.prototype.sampleFunction = function () {
            return 'sizermodel';
        };

        SizerModel.build = function (data) {
            return new SizerModel(data);
        };
        return SizerModel;
    }
]);
