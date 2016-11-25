var gulp = require('gulp');
var concat = require('gulp-concat');
var minifyCss = require('gulp-minify-css');
var uglify = require('gulp-uglifyjs');
var rename = require('gulp-rename');
var sass = require('gulp-sass');
var mocha = require('gulp-mocha');

var server_path = './server/';
var databases_path = server_path + 'databases/';
var www_path = 'www/';
var public_path = www_path + 'public/';

var mysql = require(databases_path + 'mysql/setup');

var paths = require('./env/paths').paths;

gulp.task('sass', function () {
  return gulp.src(paths.scss)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(public_path + 'css'));
});

gulp.task('css', ['sass'], function (done) {
    gulp.src(paths.css)
        .pipe(concat('bundle.js'))
        .pipe(minifyCss({
            keepSpecialComments: 0
        }))
        .pipe(rename({extname: '.min.css'}))
        .pipe(gulp.dest(public_path + 'dist/css'))
        .on('end', done);
});

gulp.task('uglify', function() {
    return gulp.src(paths.js)
        .pipe(uglify('prod.js'))
        .pipe(gulp.dest(public_path + 'dist/js/'));
});

gulp.task('buildjs', ['uglify'], function(done) {
    gulp.src(paths.jsbundle)
        .pipe(concat('bundle.js'))
        .pipe(rename({extname: '.min.js'}))
        .pipe(gulp.dest(public_path + 'dist/js'))
        .on('end', done);
});

gulp.task('stest', function () {
    return gulp.src('server/test/*.js', {read: false})
        .pipe(mocha({reporter: 'spec'}));
});

gulp.task('dbinit', function () {
    return mysql.setup();
});

gulp.task('watch', function () {
    gulp.watch(paths.scss, ['css']);
    gulp.watch(paths.js, ['buildjs']);
});

gulp.task('build', ['buildjs', 'css'])
