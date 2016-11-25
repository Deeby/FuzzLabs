var gen = require("../../../lib/gen");

module.exports = function(sequelize, DataTypes) {
    var schema = {
        'name': {
            type: DataTypes.STRING,
            allowNull: false
        },
        'email': {
            type: DataTypes.STRING,
            allowNull: false,
            unique : true
        },
        'username': {
            type: DataTypes.STRING,
            allowNull: false,
            unique : true
        },
        'public_id': {
            type: DataTypes.STRING,
            set: function (len) {
                var id = gen.gen_public_id(len);
                this.setDataValue('public_id', id);
            },
            unique: true
        }
    };

    var options = {
        associate: function(models) {
            models.user.hasOne(models.hash, {onDelete: 'cascade', hooks:true});
        }
    };

    var User = sequelize.define('user', schema, options);
    return User;
};
