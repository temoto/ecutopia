module.exports = function(grunt) {

  var stylusFiles = ['src/**/*.styl'];
  var cssFiles = ['src/**/*.css'];

  var coffeeFiles = ['src/**/*.coffee'];
  var jsFiles = ['src/**/*.js'];

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: {
      build: ['build'],
    },
    coffee: {
      compile: {
        files: {
          'build/coffee.js': coffeeFiles,
        },
      },
      options: {
        bare: false,
        join: true,
        sourceMap: true,
      },
    },
    concat: {
      css: {
        src: cssFiles.concat(['build/stylus.css']),
        dest: 'build/all.css',
      },
      js: {
        src: jsFiles.concat(['build/coffee.js']),
        dest: 'build/all.js',
      },
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd HH-MM-ss") %> */\n',
        separator: ';',
      },
    },
    jshint: {
      // define the files to lint
      files: ['gruntfile.js', 'src/**/*.js', 'test/**/*.js'],
      // configure JSHint (documented at http://www.jshint.com/docs/)
      options: {
          // more options here if you want to override JSHint defaults
        globals: {
          console: true,
          jQuery: true,
          module: true,
          smarttabs: true,
        },
      },
    },
    stylus: {
      files: {
        src: stylusFiles,
        dest: 'build/stylus.css',
      },
      options: {
        compress: false,
      },
    },
    // uglify: {
    //   options: {
    //     banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
    //   },
    //   build: {
    //     src: 'build/all.js',
    //     dest: 'build/all.min.js',
    //   },
    // },
    // qunit: {
    //   files: ['test/**/*.html'],
    // },
    watch: {
      css: {
        files: cssFiles.concat('build/stylus.css'),
        tasks: ['concat:css'],
      },
      coffee: {
        files: coffeeFiles,
        tasks: ['coffee'],
      },
      grunt: {
        files: ['gruntfile.js', 'package.json'],
      },
      js: {
        files: jsFiles.concat(['build/coffee.js']),
        tasks: ['jshint', 'concat'],
      },
      stylus: {
        files: stylusFiles,
        tasks: ['build_css'],
      },
    },
  });

  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  // grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-stylus');
  // grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-exec');

  grunt.registerTask('build_css', ['stylus']);
  grunt.registerTask('build_js', ['coffee', 'jshint', 'concat']);
  grunt.registerTask('build', ['build_css', 'build_js']);

  grunt.registerTask('test', [
    'build_js',
    // 'qunit',
  ]);

  // the default task can be run just by typing "grunt" on the command line
  grunt.registerTask('default', ['watch']);

};
