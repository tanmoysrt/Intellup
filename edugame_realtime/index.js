// ! DATABASES

// * Redis for cache
const Redis = require("ioredis");
const redis = new Redis();

// * MongoDB for message and chatlist Storage
let db = require("./db_operation/db_control");
db._connect();

const { findPlayer, addPlayer, removePlayer } = require("./db_operation/partner_request_operations");
const { addBattle, removeBattle } = require("./db_operation/battle_data_operations");
const axios = require('axios');


// ! SERVER

// * Express Server
const express = require('express');
const app = express()
app.use(express.json()); // Support JSON Request
// app.use(require("express-status-monitor")());

// * Bind httpServer with express server
const httpServer = require("http").createServer(app);

// * Bind Socket IO With HttpServer
const io = require("./server/socketServer")({httpServer:httpServer,redis:redis});

// ! Initiate Connections

// * Socket IO Connection
io.on("connection", async (socket) => {
  await require("./events/connectHandler")({socket:socket, redis: redis, axios : axios});
  require("./events/setUserNo")({socket:socket});
  require("./events/set_record_battle_id")({socket:socket});
  require("./events/setOponnentId")({socket : socket, redis : redis});
  require("./events/progressnotifier")({socket:socket, axios : axios});
  require("./events/disconnectHandler")({ socket: socket, redis: redis, axios : axios });  
});


// TODO On disconnect make another winner

async function  testing(){
  // console.log(await findPlayer({battleId : "k12345"}));
  // console.log(await addPlayer({battleId : "k12345", userId :"68868" }));
  // console.log(await removePlayer("60e2f948f257546ea92e3989"));
  // console.log(await addBattle({
  //   user1_id :"111111111",
  //   user2_id : "2222222222",
  //   battle_id : "3333333333",
  //   question_ids : [6,1,7],
  //   correct_answer_options : [2,3,1],
  //   question_answer_set : {
  //     "1": {
  //     "question": "<p>a</p>",
  //     "option1": "<p>a</p>",
  //     "option2": "<p>a</p>",
  //     "option3": "<p>a</p>",
  //     "option4": "<p>a</p>"
  //     },
  //     "6": {
  //     "question": "<p>sdffg</p>",
  //     "option1": "<p>dgdfg</p>",
  //     "option2": "<p>fdg</p>",
  //     "option3": "<p>ffdfg</p>",
  //     "option4": "<p>gffg</p>"
  //     },
  //     "7": {
  //     "question": "<p>sdfas</p>",
  //     "option1": "<p>sddd</p>",
  //     "option2": "<p>sdfssd</p>",
  //     "option3": "<p>fdgd</p>",
  //     "option4": "<p>dgggd</p>"
  //     }
  //     }
  // }));

// console.log(await removeBattle("60e301a156d5ea7f66287e90"));
}

testing()

// * Begin Listening
httpServer.listen(3000);
