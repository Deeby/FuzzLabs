var koa = require('koa');
var serve = require('koa-static');
var router = require('koa-router')();
var mysqldb = require('./databases/mysql');
var path = require('path');
var app = module.exports = koa();

mysqldb.init();

app.use(router.routes());
app.use(router.allowedMethods());

app.use(serve(path.join(__dirname, '../www/public/')));

if (!module.parent) {
    app.listen(3000);
}
var sample = require('./controllers/sample');
router.get('/sample', sample.fetch);
