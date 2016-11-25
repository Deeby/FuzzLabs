var crypto = require('crypto');

module.exports.gen_public_id = function gen_public_id(len) {
    return crypto.randomBytes(Math.ceil(len/2))
        .toString('hex')
        .slice(0, len);
};
