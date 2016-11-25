var fs = require('fs');
var path = require('path');
var Sequelize = require('sequelize');
var dbconfig = require('config').get('db');

var client;
var models = {};

module.exports.init = function () {
    client = new Sequelize(dbconfig.database, dbconfig.username, dbconfig.password, dbconfig.options);
    module.exports.client = client;
    fs
        .readdirSync(__dirname + '/models')
        .filter(function (file) {
            return (file.indexOf('.') !== 0) && (file !== 'index.js');
        })
        .forEach(function (file) {
            var model = client.import(path.join(__dirname + '/models', file));
            module.exports[model.name] = model;
            models[model.name] = model;
        });

    Object.keys(models).forEach(function (modelName) {
        if (module.exports[modelName].options.hasOwnProperty('associate')) {
            module.exports[modelName].options.associate(models);
        }
    });
};
