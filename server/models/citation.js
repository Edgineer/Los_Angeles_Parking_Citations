var mongoose = require('mongoose');

var schema = new mongoose.Schema({
 issueTime: String,
 fine: Number,
 Color: String,
 Make: String,
 violationCode: String,
 ticketNumber:String,
 issueDate:Date,
 Latitude:Number,
 bodyStyle:String,
 violationDescription:String,
 Longitude: Number,
 Location: String
});
var Citation = mongoose.model('Citation', schema);

module.exports = {Citation};