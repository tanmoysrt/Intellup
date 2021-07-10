const mongoose = require("mongoose");
const BattleModel = require("../models/battle_data");


const addBattle = async({user1_id,user2_id,battle_id, battle_history_id, question_ids, correct_answer_options, question_answer_set })=>{
    const result = await BattleModel.create({
        user1_id : user1_id,
        user2_id : user2_id,
        battle_id : battle_id,
        battle_history_id : battle_history_id,
        question_ids : question_ids,
        correct_answer_options : correct_answer_options,
        question_answer_set : question_answer_set
    })
    const res = await result.save();
    return res;
}

const removeBattle = async(id)=>{
    try {
        await BattleModel.findByIdAndDelete(id);
        return true;
    } catch (error) {
        console.log(error);
        return false;
    }
}

module.exports = {
    addBattle,
    removeBattle
}