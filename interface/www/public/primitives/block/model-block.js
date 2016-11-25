app.factory('BlockModel', [
    function() {
        function BlockModel(data) {
            _.assign(this, data);
        }

        BlockModel.prototype.sampleFunction = function () {
            return 'blockmodel';
        };

        BlockModel.build = function (data) {
            return new BlockModel(data);
        };
        return BlockModel;
    }
]);
