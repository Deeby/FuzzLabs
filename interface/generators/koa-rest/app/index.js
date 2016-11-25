'use strict';
var util = require('util');
var path = require('path');
var yeoman = require('yeoman-generator');


var KoaRestGenerator = yeoman.generators.Base.extend({
    constructor: function () {
        yeoman.Base.apply(this, arguments);
        this.argument('restname', { type: String, required: true });

    },

    generateController: function() {
        var context = {
            restName: this.restname
        };

        var path = "server/server.js",
            file = this.readFileAsString(path);

        file += "var "+this.restname+" = require('./controllers/"+this.restname+"');\n";
        file += "router.get('/"+this.restname+"', "+this.restname+".fetch);\n";
        this.write(path, file);

        this.template("rest.js", "server/controllers/"+this.restname+".js", context);
    }
});

module.exports = KoaRestGenerator;
