function setUserNo({socket}){
    socket.on("set_userno", async (data) => {
        socket.userNo = data["userNo"];
        console.log(`Userno ${socket.userNo}`);
    });
}

module.exports = setUserNo;