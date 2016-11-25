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
        this.argument('color', { type: String, required: true });
    },

    generateButtonDirective: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst(),
            primitiveColor: this.color
        };
        this.template("directive-button-primitive.js",
                      "www/public/primitives/"+this.name+"/directive-button-"+this.name+".js",
                      context);
    },

    generateItemDirective: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst(),
            primitiveColor: this.color
        };
        this.template("directive-item-primitive.js",
                      "www/public/primitives/"+this.name+"/directive-item-"+this.name+".js",
                      context);
    },

    generateModel: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst(),
            primitiveColor: this.color
        };
        this.template("model-primitive.js",
                      "www/public/primitives/"+this.name+"/model-"+this.name+".js",
                      context);
    },

    generateStyle: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst(),
            primitiveColor: this.color
        };
        this.template("primitive.scss",
                      "www/public/primitives/"+this.name+"/"+this.name+".scss",
                      context);
    },

    generateButtonView: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst(),
            primitiveColor: this.color
        };
        this.template("view-button-primitive.html.tpl",
                      "www/public/primitives/"+this.name+"/view-button-"+this.name+".html.tpl",
                      context);
    },

    generateItemView: function(){
        var context = {
            primitiveName: this.name,
            primitiveCapName: this.name.capitalizeFirst(),
            primitiveColor: this.color
        };
        this.template("view-item-primitive.html.tpl",
                      "www/public/primitives/"+this.name+"/view-item-"+this.name+".html.tpl",
                      context);
    }
});

module.exports = PrimitiveGenerator;
