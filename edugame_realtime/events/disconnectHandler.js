const {removePlayer} = require("../db_operation/partner_request_operations");
const BattleModel = require("../models/battle_data");
const {ROUTE_FOR_BATTLE_UPDATE} = require("../config");


function disconnectHandler({socket,redis,axios}){
    socket.on("disconnect", async () => {
      await redis.del(socket.userId);
      await removePlayer(socket.waitId);
      console.log(`Oponnent id : ${socket.oponnentId}`);
      if(socket.oponnentId != undefined ){
        console.log(`Userno at the time of disconnect : ${socket.userNo}`);
        var battleRecord = await BattleModel.findById(socket.battleRecordId);

        if(socket.userNo == 1 && !battleRecord.user1_is_submitted){
          console.log(`Leaving user1 battleidreal ${socket.battleRecordId}`)
          await BattleModel.findByIdAndUpdate(socket.battleRecordId,{
            user1_is_submitted : true,
            user1_answer_ids : Array.from({length: battleRecord.question_ids.length}, (_, i) => -1),
            user_1_skipped : true
          })
        }
        
        if(socket.userNo == 2 && !battleRecord.user2_is_submitted){
                    console.log(`Leaving user2 battleidreal ${socket.battleRecordId}`)

          await BattleModel.findByIdAndUpdate(socket.battleRecordId,{
            user2_is_submitted : true,
            user2_answer_ids : Array.from({length: battleRecord.question_ids.length}, (_, i) => -1),
            user_2_skipped : true
          })
        }

        battleRecord = await BattleModel.findById(socket.battleRecordId);

        if(battleRecord.user_1_skipped && battleRecord.user_2_skipped){
          var payload = {
            "battle_history_id" : battleRecord.battle_history_id,
            "winner_user_id" : "00000000-0000-0000-0000-000000000000",
            "user1_answers" : battleRecord.user2_answer_ids,
            "user2_answers" : battleRecord.user2_answer_ids,

        }

        while(true){
            try{
                await axios.post(ROUTE_FOR_BATTLE_UPDATE,JSON.stringify(payload));
                break;
            }
            catch(e){
                console.log(e);
                console.log("Going in loop on disconnect hisroy updatw");
            }
        }
      }
      }

      console.log(`Disconnected..... User ID : ${socket.userId} Battle ID : ${socket.battleId}`);
    });
}

module.exports = disconnectHandler;