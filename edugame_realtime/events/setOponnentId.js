function setOponnentId({socket,redis}){
    socket.on("set_oponnent_id", async (data) => {

        const oponnentId = await redis.get(data["userId"]);
        socket.oponnentUserId = data["userId"];
        socket.oponnentId = oponnentId;

        console.log(data);
        console.log(`Oponnent ID : ${socket.oponnentId}`);
    });
}

module.exports = setOponnentId;