const mongoose = require("mongoose");
const BattleModel = require("../models/battle_data");
const {ROUTE_FOR_BATTLE_UPDATE,ROUTE_FOR_BATTLE_END_REDIRECTION} = require("../config");

function progressNotifier({socket, axios}){

    socket.on("notify_answer_submission", async(data) =>{
        // Need to send only the no of questions submitted => data [int]
        socket.to(socket.oponnentId).emit("oponnent_progress",{
            "submitted" : false,
            "no_of_questions_submitted" : data
        });
    });


    socket.on("submit_answer", async(data) =>{
        // Need to send the list of questions option [!! NOTE not index !!] submitted => data [List<int>]
        socket.to(socket.oponnentId).emit("oponnent_progress",{
            "submitted" : true,
            "no_of_questions_submitted" : data.length
        });

        if (socket.userNo == 1){
            await BattleModel.findByIdAndUpdate(socket.battleRecordId,{user1_answer_ids : data,user1_is_submitted : true});
        }
        else if(socket.userNo == 2){
            await BattleModel.findByIdAndUpdate(socket.battleRecordId,{user2_answer_ids : data,user2_is_submitted : true});
        }

        const battleRecord = await BattleModel.findById(socket.battleRecordId);
       
        // "battle_history_id" , "winner_user_id", "user1_answers", "user2_answers"
        if(battleRecord.user1_is_submitted && battleRecord.user2_is_submitted){
            var user1answerlist = battleRecord.user1_answer_ids;
            var user2answerlist = battleRecord.user2_answer_ids;
            var correctanswers = battleRecord.correct_answer_options;
            var user1score = 0 ;
            var user2score = 0 ;
            var winner_user_id ;

            for(var i = 0; i< correctanswers.length; i++){
                if(user1answerlist[i] == correctanswers[i]){
                    user1score = user1score + 1;
                }
                if(user2answerlist[i] == correctanswers[i]){
                    user2score = user2score + 1;
                }
            }

            if(user1score > user2score){
                winner_user_id = battleRecord.user1_id;
            }
            else if(user2score > user1score){
                winner_user_id = battleRecord.user2_id;
            }
            else if(user1score == user2score){
                winner_user_id = "00000000-0000-0000-0000-000000000000";
            }

            var payload = {
                "battle_history_id" : battleRecord.battle_history_id,
                "winner_user_id" : winner_user_id,
                "user1_answers" : user1answerlist,
                "user2_answers" : user2answerlist,

            }

            while(true){
                try{
                    await axios.post(ROUTE_FOR_BATTLE_UPDATE,JSON.stringify(payload));
                    break;
                }
                catch{
                    console.log("Going in loop");
                }
            }

            socket.to(socket.oponnentId).emit("quitgame",{
                "redirect_link" : `${ROUTE_FOR_BATTLE_END_REDIRECTION}${battleRecord.battle_history_id}/`
            });
            socket.emit("quitgame",{
                "redirect_link" : `${ROUTE_FOR_BATTLE_END_REDIRECTION}${battleRecord.battle_history_id}`
            });
        }

    });


    }
    
    module.exports = progressNotifier;