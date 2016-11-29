'use strict';
var util = require('util');
var path = require('path');
var yeoman = require('yeoman-generator');

String.prototype.capitalizeFirst = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

var PrimitiveGenerator = yeoman.generators.Base.extend({
    constructor: function () {
        yeoman.Base.apply(this, arguments);
        this.argument('name', { type: String, required: true });
        this.argument('bgcolor', { type: String, required: true });
        this.argument('fgcolor', { type: String, required: true });
    },

    generateButtonDirective: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst()
        };
        this.template("directive-button.js",
                      "www/public/primitives/"+this.name+"/directive-button-"+this.name+".js",
                      context);
    },

    generateItemDirective: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst()
        };
        this.template("directive-item.js",
                      "www/public/primitives/"+this.name+"/directive-item-"+this.name+".js",
                      context);
    },

    generatePropertiesDirective: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst()
        };
        this.template("directive-properties.js",
                      "www/public/primitives/"+this.name+"/directive-properties-"+this.name+".js",
                      context);
    },

    generateStyle: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst(),
            primitiveBgColor: this.bgcolor,
            primitiveFgColor: this.fgcolor
        };
        this.template("primitive.scss",
                      "www/public/primitives/"+this.name+"/"+this.name+".scss",
                      context);
    },

    generateButtonView: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst()
        };
        this.template("view-button.html.tpl",
                      "www/public/primitives/"+this.name+"/view-button-"+this.name+".html.tpl",
                      context);
    },

    generateItemView: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst()
        };
        this.template("view-item.html.tpl",
                      "www/public/primitives/"+this.name+"/view-item-"+this.name+".html.tpl",
                      context);
    },

    generatePropertiesView: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst()
        };
        this.template("view-properties.html.tpl",
                      "www/public/primitives/"+this.name+"/view-properties-"+this.name+".html.tpl",
                      context);
    }

});

module.exports = PrimitiveGenerator;
