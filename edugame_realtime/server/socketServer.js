
function socketServer({httpServer,redis}){
    let io = require("socket.io")(httpServer, { cors: { origin: "*" } });
    io = require("../middleware/socketAuthMiddleware")({ io: io, redis: redis });
    return io;
}

module.exports = socketServer;