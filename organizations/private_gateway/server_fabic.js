var express = require('express'),
app = express()
var session = require('express-session');   
var path = require('path');
var bodyParser = require('body-parser');
var port = 8000
// 
// require('dotenv').config();
var cors = require('cors');
app.use(cors());

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.set("view engine","ejs");

var routes = require('./routes.js'); //importing route
app.use(routes)

app.use(function(req, res) {
    res.status(404).send({url: req.originalUrl + ' not found'})
}) 



app.listen(port);

console.log('Server run with port =  ' + port);
module.exports = app;