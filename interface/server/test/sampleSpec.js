'use strict';
var superagent = require('supertest');
var assert = require('assert');
var app = require('../server');

var userAgent = superagent.agent(app.listen());

describe.only('Sample', function () {
    it('should return with ok', function (done) {
        userAgent
            .get('/sample')
            .end(function(err, result) {
                assert.equal(result.status, 200);
                assert.equal(result.body.test, 'ok');
                done();
            });
    });
});
