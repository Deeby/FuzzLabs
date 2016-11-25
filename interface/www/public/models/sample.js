app.factory('User', [
    function() {
        function User(data) {
            _.assign(this, data);
        }

        User.prototype.sampleFunction = function () {
            return 'sample';
        };

        User.build = function (data) {
            return new User(data);
        };
        return User;
    }
]);
