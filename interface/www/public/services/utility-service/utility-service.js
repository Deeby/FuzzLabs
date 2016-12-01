app.factory('utilityService', [
    function() {

        // Convert a decimal number to hexadecimal string.
        // If prefix is set to 'true' the result will be
        // prefixed with '0x'.

        this.toHex = function(value, prefix) {
            value = value.toString(16);
            var pfix = "0x";
            if (value.length % 2) value = ("0" + value);
            if (prefix !== true) pfix = "";
            return pfix + value.toUpperCase();
        }

        // Convert a decimal number into it's ascii 
        // representation.

        this.toAscii = function(value) {
            if (value > 255 || value < 0) return "";
            return String.fromCharCode(value);
        }

        this.uuid = function() {
            var fmt = 'xxxxxxxx-xxxx-xxxx-yxxx-xxxxxxxxxxxx';
            return fmt.replace(/[xy]/g, function(c) {
                var r = Math.random()*16|0, v = c === 'x' ? r : (r&0x3|0x8);
                return v.toString(16);
            });
        }

        return this;
    }
]);
