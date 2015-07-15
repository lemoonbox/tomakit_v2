var gulp = require('gulp');

var server = require('gulp-webserver'); //this is not needed in this project
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var minifyhtml = require('gulp-minify-html');
var minifycss = require('gulp-minify-css');
var sass = require('gulp-sass');
var livereload = require('gulp-livereload');
var gutil = require('gulp-util');
var del = require('del');
//var sassFiles = 'public/src/scss/**/*.scss';

var src = 'public/src';
var dist = 'public/dist';

var paths = {
    js: src + '/js/*.js',
    scss: src + '/scss/*.scss',
    html: src + '/**/*.html'
};

//clean files
gulp.task('clean', function(cb){
    del(['public/dist/css/*'], cb);
});

//localhost:8000
gulp.task('server', function() {
    return gulp.src(dist + '/')
        .pipe(server());
});

//combine javascript files
gulp.task('combine-js', function () {
    return gulp.src(paths.js)
        .pipe(concat('script.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist' + '/js'));
});

//compile sass files to css
gulp.task('sass', function() {
  return gulp.src(paths.scss)
  .pipe(sass({
    errLogToConsole: true
  }))
  .pipe(minifycss())
  .pipe(gulp.dest(dist + '/css'))
      .on('error', gutil.log)
      //reload browser
      //.pipe(pulgins.autoprefixer(
      //    {
      //        browsers: [
      //            '> 1%',
      //            'last 2 versions',
      //            'firefox >= 4',
      //            'safari 7',
      //            'safari 8',
      //            'IE 8',
      //            'IE 9',
      //            'IE 10',
      //            'IE 11'
      //        ],
      //        cascade:false
      //    }
      //))
      .pipe(livereload());
});

//minify html files
gulp.task('compress-html', function() {
    return gulp.src(paths.html)
        .pipe(minifyhtml())
        .pipe(gulp.dest(dist + '/'));
});

//auto reload browser when files change
gulp.task('watch', function() {
    //plugins.
    //livereaload.listen();
    gulp.watch(paths.js, ['combine-js']);
    gulp.watch(paths.scss, ['sass']);
    //gulp.watch(paths.html, ['compress-html']);
    gulp.watch(dist + '/**').on('change', livereload.changed);
});

//set default task
gulp.task('default', [
    //'server',
    'clean', 'combine-js',
    'sass',
    'compress-html',
    'watch'
]);