const {addPlayer, findPlayer, removePlayer} = require("../db_operation/partner_request_operations");
const {ROUTE_FOR_RANDOM_QUESTIONS, ROUTE_FOR_BATTLE_DETAILS, ROUTE_FOR_BATTLE_REGISTER} = require("../config");
const { addBattle } = require("../db_operation/battle_data_operations");


async function connectHandler({socket, redis, axios}){
    console.log(`Connected...  User ID : ${socket.userId} Battle ID : ${socket.battleId}`);

    var res = await findPlayer(socket.battleId);
    if(res){
        // Check whether someone waiting or not
        // console.log(res);
        await removePlayer(res._id);
        const oponnentId = await redis.get(res.userId);
        socket.oponnentUserId = res.userId;
        socket.oponnentId = oponnentId;
        
        // Notify user that he has got an participant
        socket.to(oponnentId).emit("found_confirm",{
            "message" : "Oponnent Has Been Found.",
        });

        socket.emit("found_confirm",{
            "message" : "Oponnent Has Been Found.",
        });

        // This is to identify who is user 1 and who is user 2
        socket.userNo = 1;
        socket.to(oponnentId).emit("new_userno",{
            "message" : "Setting User No to 2",
            "userNo" : 2,
        });


        socket.emit("notify_match",{
            id : res.id,
            userId : res.userId
        });

        socket.to(oponnentId).emit("notify_match",{
            id : socket.id,
            userId : socket.userId
        });

        // After this  show two users that question is loading

        var response_questions,response_category_details, user1_id, user2_id, no_of_questions, max_time , battle_history_id;

        // 1 -> Load battle category details
        while(true){
            try{
                response_category_details = await axios.get(ROUTE_FOR_BATTLE_DETAILS+socket.battleId+"/");
                response_category_details = response_category_details.data;
                no_of_questions = response_category_details["no_of_questions"];
                max_time = response_category_details["max_time"];
                // console.log(response_category_details);
                break;
            }
            catch(e){
                console.log(`Error ${e}`);
                console.log("Again looping");
            }
        };
        // 2 -> Load questions

        while(true){
            try{
                response_questions = await axios.get(ROUTE_FOR_RANDOM_QUESTIONS+no_of_questions+"/"+socket.school_classId+"/"+socket.school_subjectId);
                response_questions = response_questions.data;
                // console.log(response_questions);
                break;
            }
            catch(e){
                console.log(`Error ${e}`);
                console.log("Again looping");
            }
        };
        // 3 -> identify user1 and user2
         
        if (socket.userNo == 1){
            user1_id = socket.userId;
            user2_id = socket.oponnentUserId;
        }
        else if(socket.userNo == 2){
            user1_id = socket.oponnentUserId;
            user2_id = socket.userId;
        };

        const payload_for_main_server = {
            "user1_id" : user1_id,
            "user2_id" : user2_id,
            "battle_id" : socket.battleId,
            "questions" : response_questions.question_ids
        }

        var response_battle_history;
        while(true){
            try{
                response_battle_history  = await axios.post(ROUTE_FOR_BATTLE_REGISTER,JSON.stringify(payload_for_main_server));
                response_battle_history = response_battle_history.data;
                if(response_battle_history.success == true){
                    battle_history_id = response_battle_history.battle_history_id
                    break;
                }
            }
            catch{
                console.log("Going in loop");
            }
        }
        // console.log(response_battle_history);

        const mongo_battle_record_realtime = await addBattle({
            user1_id : user1_id,
            user2_id : user2_id,
            battle_id : socket.battleId,
            battle_history_id : battle_history_id,
            question_ids : response_questions.question_ids,
            correct_answer_options : response_questions.correct_answer_options,
            question_answer_set : response_questions.question_answer_set
        });


        socket.battleRecordId =  mongo_battle_record_realtime._id;

        // Let's start quiz
        socket.to(socket.oponnentId).emit("start_quiz",{
            question_answer_set : mongo_battle_record_realtime.question_answer_set,
            realtime_battle_id : mongo_battle_record_realtime._id,
        });

        socket.emit("start_quiz",{
            question_answer_set : mongo_battle_record_realtime.question_answer_set,
            realtime_battle_id : mongo_battle_record_realtime._id,
        });


    }else{
        // Create record 
        socket.waitId = await addPlayer({
            userId : socket.userId,
            battleId : socket.battleId
        });

        socket.emit("wait_for_player",{
            "message" : "No Matching player not found .Please Wait"
        });
    }

}

module.exports = connectHandler;