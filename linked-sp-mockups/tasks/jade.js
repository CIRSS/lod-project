/**
 * grunt-contirb-jade options
 * @type {Object}
 */

module.exports = {
  html: {
    files: [{
      expand: true,
      cwd: '<%= folders.app %>/jade',
      src: ['index.jade', 'motley/*jade', 'proust/*jade'],
      dest: '.tmp/',
      ext: '.html'
    }],
    options: {
    data: function(dest, src) {
            // Data is returned for the json file in the same folder
            // with the same name as the jade file
            try {
                return require("../"+src[0].split(".")[0]+".json");
            } catch (e) {
                if (e.name === 'Error') {
                    return {}
                } else {
                    throw e;
                }
            }
            },
      client: false,
      pretty: true,
      basedir: '<%= folders.app %>/jade'
    }
  }
};
