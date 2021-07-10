function setRecordBattleId({socket}){
    socket.on("set_battle_record_id", async (data) => {
        socket.battleRecordId = data["battleRecordId"];
        console.log(data);
        console.log(`Battle ID : ${socket.battleRecordId}`);
    });
}

module.exports = setRecordBattleId;