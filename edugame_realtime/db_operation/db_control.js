const mongoose = require('mongoose');
const {MONGODB_SERVER,MONGODB_DATABASE} = require("../config");

class Database {
  
_connect() {
     mongoose.connect(`mongodb://${MONGODB_SERVER}/${MONGODB_DATABASE}`,{
      useUnifiedTopology: true,
      useNewUrlParser: true,
      useFindAndModify : false
     })
       .then(() => {
         console.log('Database connection successful')
       })
       .catch(err => {
         console.error('Database connection error')
       })
  }
}

module.exports = new Database()