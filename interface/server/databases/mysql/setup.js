var mysqldb = require('./');

module.exports.setup = function() {
    mysqldb.init();
    mysqldb.client.sync({force: false});
}
