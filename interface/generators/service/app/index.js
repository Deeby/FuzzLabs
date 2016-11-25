'use strict';
var util = require('util');
var path = require('path');
var yeoman = require('yeoman-generator');


var ServicesGenerator = yeoman.generators.Base.extend({
    constructor: function () {
        yeoman.Base.apply(this, arguments);
        this.argument('servicename', { type: String, required: true });
    },

    generateController: function(){
        var context = {
            serviceName: this.servicename
        };

        this.template("service.js", "www/public/services/"+this.servicename+"/"+this.servicename+".js", context);

    }
});

module.exports = ServicesGenerator;
