module.exports = function(sequelize, DataTypes) {
    // Password is of type DataTypes.BLOB to store
    // scrypt binary hash.
    var schema = {
        uuid: {
            type: DataTypes.UUID,
            defaultValue: function() {
                return security.genPublicId(32)
            },
            primaryKey: true
        },
        'password': {
            type: DataTypes.BLOB,
            allowNull: false
        }
    };

    var options = {
        associate: function(models) {
            models.hash.belongsTo(models.user);
        }
    };

    var Hash = sequelize.define('hash', schema, options);
    return Hash;
};
