'use strict'

var server_path = './server';
var databases_path = server_path + 'databases/';
var www_path = 'www/';
var public_path = www_path + 'public/';

module.exports.paths = {
    server_path: server_path,
    databases_path: databases_path,
    www_path: www_path,
    public_path: public_path,
    scss: [
        www_path + 'scss/**/*.scss',
        www_path + 'scss/*.scss',
        public_path + 'modules/*/*.scss',
        public_path + 'directives/*/*.scss',
        public_path + 'primitives/*/*.scss',
        public_path + 'primitives/*.scss'
    ],
    css: [
        public_path + 'css/*.css',
        public_path + 'css/**/*.css',
        public_path + 'bower_components/angular-material/angular-material.css',
        public_path + 'bower_components/animate.css/animate.css'
    ],
    js: [
        public_path + 'app.js',
        public_path + 'modules/*/!(*-*).js',
        public_path + 'modules/*/*.js',
        public_path + 'directives/*/*.js',
        public_path + 'services/*/*.js',
        public_path + 'models/*.js',
        public_path + 'primitives/*/*.js'
    ],
    jsbundle: [
        public_path + 'bower_components/angular/angular.js',
        public_path + 'bower_components/angular-route/angular-route.js',
        public_path + 'bower_components/angular-material/angular-material.js',
        public_path + 'bower_components/angular-animate/angular-animate.js',
        public_path + 'bower_components/angular-aria/angular-aria.js',
        public_path + 'bower_components/lodash/lodash.js',
        public_path + 'bower_components/moment/min/moment.js',
        public_path + 'bower_components/ng-file-upload/ng-file-upload-all.js',
        'bower_components/paralleljs/lib/parallel.js',
        'bower_components/angular-parallel/index.js',
        public_path + 'dist/js/prod.js',
    ],
    models: [
        databases_path + '/mysql/models/*.js'
    ]
};
