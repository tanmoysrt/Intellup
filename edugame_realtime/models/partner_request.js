const mongoose = require("mongoose");

const partner_request_schma = new mongoose.Schema({
  userId: {
    type: String,
    required: true,
  },
  battleId: {
    type: String,
    required: true,
  }
},
  {
    timestamps: true
}
);


module.exports = mongoose.model("PartnerRequest", partner_request_schma);
