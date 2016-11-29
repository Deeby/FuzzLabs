var spawn = require('child_process').spawn;
var primitives = require('./primitives.json');

primitives.forEach(function(primitive) {
    console.log("Building primitive: " + primitive.primitive);
    var rc = spawn('yo', ['primitive', 
        primitive.primitive, 
        primitive.color.background, 
        primitive.color.foreground
    ]);
    /*
    rc.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
    */
});

