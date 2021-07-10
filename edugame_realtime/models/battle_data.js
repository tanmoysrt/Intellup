const mongoose = require("mongoose");

const battle_data_schema = new mongoose.Schema({
  user1_id: {
    type: String,
    required: true,
  },
  user2_id: {
    type: String,
    required: true,
  },
  battle_id: {
    type: String,
    required: true,
  },
  battle_history_id :{
    type : String,
    required : true,
  },
  question_ids : {
      type : [],
      required : true
  },
  user1_answer_ids : {
    type : [],
    required : false,
    default :[]
  },
  user1_is_submitted : {
    type : Boolean,
    required : false,
    default : false
  },
  user2_is_submitted : {
    type : Boolean,
    required : false,
    default : false
  },
  user2_answer_ids : {
    type : [],
    required : false,
    default :[]
  },
  correct_answer_options : {
      type : [],
      required : true
  },
  question_answer_set : {
      type : {},
      required : true
  },
  user_1_skipped : {
    type : Boolean,
    required : false,
    default : false
  },
  user_2_skipped : {
    type : Boolean,
    required : false,
    default : false
  },
},
  {
    timestamps: true
}
);


module.exports = mongoose.model("BattleData", battle_data_schema);
