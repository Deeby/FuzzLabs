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

        return this;
    }
]);
