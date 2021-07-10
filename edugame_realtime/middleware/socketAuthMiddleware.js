// will need to implement later

function auth({io,redis}){
    io.use((socket, next) => {
        const userId = socket.handshake.auth.userId;
        const battleId = socket.handshake.auth.battleId;
        const classId = socket.handshake.auth.classId;
        const subjectId = socket.handshake.auth.subjectId;
        redis.set(userId, socket.id);
        if (!userId && !battleId) {
          return next(new Error("invalid currentUserId"));
        }
        socket.userId = userId;
        socket.battleId = battleId;
        socket.school_classId = classId;
        socket.school_subjectId = subjectId;
        next();
      });
    return io;
}

module.exports = auth;