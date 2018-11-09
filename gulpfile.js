/*!
 * Based on UnderTasker
 * Copyright 2018 Tyler Rilling
 * Licensed under MIT (https://github.com/underlost/Undertasker/blob/master/LICENSE)
 */

// grab our packages
var gulp = require('gulp'),
    webpack = require('webpack-stream');
    jshint = require('gulp-jshint');
    sass = require('gulp-sass');
    sourcemaps = require('gulp-sourcemaps');
    concat = require('gulp-concat');
    autoprefixer = require('gulp-autoprefixer');
    cleanCSS = require('gulp-clean-css');
    rename = require('gulp-rename'); // to rename any file
    uglify = require('gulp-uglify-es').default;
    del = require('del');
    stylish = require('jshint-stylish');
    runSequence = require('run-sequence');
    coffee = require('gulp-coffee');
    gutil = require('gulp-util');
    imagemin = require('gulp-imagemin');
    git = require('gulp-deploy-git');
    gulpWebpack = require('webpack-stream');

// Cleans the web dist folder
gulp.task('clean', function () {
  return del([
    'dist/',
    'server/static/site',
    'server/static/admin',
    'server/**/*.pyc'
  ]);
});

// Clear cache
gulp.task('clean-cache', function () {
  del(['server/**/*.pyc']);
});

gulp.task('copy-dist', function() {
  gulp.src('dist/**/*.*')
  .pipe(gulp.dest('server/static'));
});

// Copy fonts task
gulp.task('copy-fonts', function() {
  gulp.src('server/static_source/fonts/site/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/fonts'));
  gulp.src('node_modules/components-font-awesome/webfonts/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/fonts'));
});
gulp.task('admin-fonts', function() {
  gulp.src('server/static_source/fonts/admin/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/admin/fonts'));
  gulp.src('node_modules/components-font-awesome/webfonts/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/admin/fonts'));
});

// Minify Images
gulp.task('imagemin', function() {
  return gulp.src('server/static_source/img/site/**/*.{jpg,png,gif,ico}')
  .pipe(imagemin())
  .pipe(gulp.dest('dist/img'))
});

// Copy component assets
gulp.task('install', function() {
  gulp.src('node_modules/components-font-awesome/scss/**/*.*')
  .pipe(gulp.dest('server/static_source/sass/_shared/font-awesome'));

  gulp.src('node_modules/bootstrap/scss/**/*.*')
  .pipe(gulp.dest('server/static_source/sass/_shared/bootstrap'));
});

// Compile coffeescript to JS
gulp.task('brew-coffee', function() {
  return gulp.src('server/static_source/coffee/*.coffee')
  .pipe(coffee({bare: true}).on('error', gutil.log))
  .pipe(gulp.dest('server/static_source/js/coffee/'))
});

// CSS Build Task for main site/theme
gulp.task('build-css', function() {
  return gulp.src('server/static_source/sass/site.scss')
  .pipe(sass().on('error', sass.logError))
  .pipe(autoprefixer({
    browsers: ['last 2 versions'],
    cascade: false
  }))
  .pipe(gulp.dest('dist/css'))
  .pipe(cleanCSS())
  .pipe(rename('site.min.css'))
  .pipe(gulp.dest('dist/css'))
  .on('error', sass.logError)
});

// Concat All JS into unminified single file
gulp.task('concat-js', function() {
  return gulp.src([
    'node_modules/jquery/dist/jquery.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/pace-progress/pace.js',
    'server/static_source/js/site.js',
    'server/static_source/js/coffee/*.*',
  ])
  .pipe(sourcemaps.init())
  .pipe(concat('site.js'))
  .pipe(sourcemaps.write('./maps'))
  .pipe(gulp.dest('dist/js'));
});

// configure the jshint task
gulp.task('jshint', function() {
  return gulp.src('server/static_source/js/site/*.js')
  .pipe(jshint())
  .pipe(jshint.reporter('jshint-stylish'));
});

// Shrinks all the site js
gulp.task('shrink-js', function() {
  return gulp.src('dist/js/site.js')
  .pipe(uglify())
  .pipe(rename('site.min.js'))
  .pipe(gulp.dest('dist/js'))
});

// Javascript build task for frontend
gulp.task('build-js', function(callback) {
  runSequence('concat-js', 'shrink-js', callback);
});

// configure which files to watch and what tasks to use on file changes
gulp.task('watch', function() {
  gulp.watch('server/static_source/coffee/**/*.js', ['brew-coffee', 'copy-dist']);
  gulp.watch('server/static_source/js/**/*.js', ['build-js', 'admin-build-js', 'copy-dist']);
  gulp.watch('server/static_source/sass/**/*.scss', ['build-css', 'admin-build-css', 'copy-dist' ] );
});

// Build task for theme/frontend
gulp.task('build', function(callback) {
  runSequence(
    ['build-css', 'build-js'], 'imagemin', 'copy-dist', callback
  );
});

// Default task will build both assets.
gulp.task('default', ['install', 'build']);
