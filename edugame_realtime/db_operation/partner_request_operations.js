const mongoose = require("mongoose");
const PartnerRequestModel = require("../models/partner_request");

const findPlayer = async(battleId) =>{
    const result = await PartnerRequestModel.find({battleId : battleId},"userId battleId");

    return result[0];
}

const addPlayer = async({userId,battleId})=>{
    const result = await PartnerRequestModel.create({
        userId : userId,
        battleId : battleId
    })
    const res = await result.save();
    return res._id;
}

const removePlayer = async (id)=>{
    try {
        await PartnerRequestModel.findByIdAndDelete(id);
        return true;
    } catch (error) {
        console.log(error);
        return false;
    }
}

module.exports = {
    findPlayer,
    addPlayer,
    removePlayer
}