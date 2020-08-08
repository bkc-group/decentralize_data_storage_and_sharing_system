


const express = require('express');
const app = express();
const bodyParser = require('body-parser');
app.use(bodyParser.json());
const request = require('request')
const uuid = require('uuid/v1');
const nodeAddr = uuid();
const port = 3000

const reqPromise = require('request-promise');
// -----------------------------

var leader = null
var list_follower = []
// var list_candidate = []

var list_candidate = [
  'http://127.0.0.1:3001'
]

app.get('/test', function (req, res) {
    console.log("canhtuan")
});


app.post('/join', function (req, res) {
    const follower = req.body.follower;
    urlFollower = "http://127.0.0.1:" + follower;
    if (list_follower.length == 0) {
    	list_follower.push(urlFollower)
    	console.log(list_follower)
    	return res.status(200).send({"msg":"tham gia thanh cong"})
    }
    list_follower.forEach(index => {
    	
    	if (index == urlFollower) {
    		return res.status(200).send({"msg":"ban da tham gia roi"})
    	}
        list_follower.push(urlFollower)
    });
    console.log(list_follower)
    return res.status(200).send({"msg":"tham gia thanh cong"})
});

app.post('/cadidate', function (req, res) {
    const candidate  = req.body.candidate;
    url_candidate = "http://127.0.0.1:" + candidate;
    // for (var i = 0; i < list_follower.length; i++) {
    // 	if (list_follower[i] == url_candidate) {
    // 		return res.status(200).send({"msg":"Ban khong co trong danh sach ung cu vien tiem nang"})
    // 	}
    // }
    if (list_candidate.length == 0) {
    	list_candidate.push(url_candidate)
    	console.log(list_candidate)
    	return res.status(200).send({"msg":"Tham gia  ung cu vien thanh cong"})
    }
   
    for (var i = 0; i < list_candidate.length; i++) {
    	if (list_candidate[i] == url_candidate) {
    		console.log(list_candidate[i])
    		return res.status(200).send({"msg":"ban da tham gia roi"})
    	}
    }
    list_candidate.push(url_candidate)
    console.log(list_candidate)
    return res.status(200).send({"msg":"Tham gia thanh cong"})
});

async function createRequest(url){
  var data = await request.get(url, {
      }, (error,result) => { 
        if (error) {
          return error
        }
        return result
  })
  console.log("test",data)
  return data

}
app.get('/leader', async function (req, res) {
   var time_start = new Date().getTime();
   console.log(time_start)
   console.log(list_candidate)
   const random_leader = list_candidate[Math.floor(Math.random() * list_candidate.length)];
   leader = random_leader
   console.log(random_leader)
   request.get(leader + "/run_worker", {
      }, (error,result) => { 
        if (error) {
          return error
        }
        return result
    })
});




function run(){
  setInterval(function(){ 
    console.log("leader la",leader)
    if(leader === null){
      
      request.get("http://127.0.0.1:3000/leader", {
          }, (error,result) => { 
            if (error) {
              console.log(error)
            }
            return result
        })
    }
    request.get(leader + "/active", {
      }, (error,result) => { 
        if (error) {
           request.get("127.0.0.1:3000/leader", {
              }, (error,result) => { 
                if (error) {
                  leader = null
                }
                return result
            })
        }
        return result
    })

  }, 3000);
}

run()


app.listen(port, function () {
    console.log(`> listening on port ${port}...`);
});