//Library Imports
var express = require('express');
var bodyParser = require('body-parser');

//Local Imports
var {mongoose} = require('./db/mongoose');
var {Citation} = require('./models/citation');

var app = express();
const port = process.env.PORT || 3000;
app.use(bodyParser.json());

//GET /citations/latitude/longitude
app.get('/citations/:usrLat/:usrLon',(req,res)=>{
	var usrLat = Number(req.params.usrLat);
	var usrLon = Number(req.params.usrLon);
	Citation.find({Latitude:{$gte:usrLat-0.05, $lte:usrLat+0.05},Longitude:{$gte:usrLon-0.05,$lte:usrLon+0.05}}).then((citations)=>{
		//empty citations array, no match in the query
		if (!citations.length) {
			return res.status(404).send();
		}
		//return matching citation array in a object
		res.send({citations});
	}, (e)=>{
		//other error
		res.status(400).send();
	});
});

app.listen(port, () => {
	console.log(`Started up at port ${port}`);
});

module.exports = {app};