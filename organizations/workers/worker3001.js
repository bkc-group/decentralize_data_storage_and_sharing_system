
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
app.use(bodyParser.json());

const uuid = require('uuid/v1');
const nodeAddr = uuid();
const port = 3001
const Web3      =   require('web3');
abi = require('../abi/abi.json')
addressContract = "0x113405659541Cf753597D29A9B595b79Cb7229B8"
const web3      = new Web3(new Web3.providers.HttpProvider("https://ropsten.infura.io/v3/66092b83a4de4330b7cc5df887e3ae4b"))
const web3_socket = new Web3(new Web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws/v3/66092b83a4de4330b7cc5df887e3ae4b"))
const Const = require('../config/const')
const request = require('request')
var querystring = require('querystring');


// Day la config --------------------------------------------------
address = "0xe4680B5B373b9353AF87De622a6E410E067a25c9"
privateKey = "ef0be3ad9cf6ab09b1aaca99e1880546e4ca82e159a590291d0ec67e5929d0cf"
contract = new web3.eth.Contract(abi, addressContract)
const ORG_NAME = Const.ORG_NAME || 'canhtuan1'
const urlpost = "http://127.0.0.1:8000/api/push/data/external/blockchain"
console.log(urlpost)
console.log("worker cua to chuc ",ORG_NAME)
const reqPromise = require('request-promise');
// -----------------------------

var leader = null
var list_follower = []
// var list_candidate = []


app.get('/test', function (req, res) {
    console.log("canhtuan")
});

app.get('/active', function (req, res) {
    console.log("ahihi")
    return res.status(200).send({"status":200,"msg":"active"})
});


async function listenContract(){

  const eventContract = new web3_socket.eth.Contract(abi, addressContract)
  eventContract.events.Metadata(async (err, events) => {
      
      console.log(events.returnValues)
      console.log(events.returnValues.org_dest)

      if(events.returnValues.org_dest == ORG_NAME){
        var seconds = new Date().getTime() / 1000
        
        var cid = events.returnValues.cid
        var org_src = events.returnValues.org_src
        var org_dest = events.returnValues.org_dest
        var user_from = events.returnValues.user_from
        var user_to = events.returnValues.user_to
        
        var form = {
          cid: cid,
          src: org_src,
          dest: org_dest,
          from: user_from,
          to: user_to
        };
        var formData = querystring.stringify(form);
        var contentLength = formData.length;

        request.post(urlpost, {
          json: {
            cid: cid,
            org_src: org_src,
            org_dest: org_dest,
            user_from: user_from,
            user_to: user_to
          }
          }, (error,result) => {
            
            console.log(error)
            console.log("Thanh Cong")
          })

      }

  })
}

app.get('/run_worker', function (req, res) {
    listenContract()
});

app.listen(port, function () {
    console.log(`> listening on port ${port}...`);
});