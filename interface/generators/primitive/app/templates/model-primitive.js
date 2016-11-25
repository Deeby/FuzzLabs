app.factory('<%= primitiveCapName %>Model', [
    function() {
        function <%= primitiveCapName %>Model(data) {
            _.assign(this, data);
        }

        <%= primitiveCapName %>Model.prototype.sampleFunction = function () {
            return '<%= primitiveName %>model';
        };

        <%= primitiveCapName %>Model.build = function (data) {
            return new <%= primitiveCapName %>Model(data);
        };
        return <%= primitiveCapName %>Model;
    }
]);
