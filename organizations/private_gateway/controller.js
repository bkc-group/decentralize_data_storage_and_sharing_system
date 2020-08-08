const { check, body, param, validationResult }  = require('express-validator');
var invokeService = require('../../fabcar/javascript/invoke');
var queryService = require('../../fabcar/javascript/query');



module.exports = ({

	createInMetaData: async (req, res, next) => {
		try {
			let fromUser = req.body.user_from;
			let toUser = req.body.user_to;
			let cid = req.body.cid;
			let time = req.body.time
			
 			// console.log(fromUser,toUser,cid)
			const errors = validationResult(req);
			if (!errors.isEmpty()) {
                let error = errors.errors
				let object = {
					"status" : 500,
					error
				}
				return res.status(200).send({object})
            }

            var key = toUser + cid
			var result = await invokeService.createInMetaData(key, fromUser, cid, toUser);
			seconds = new Date().getTime() / 1000
			console.log(seconds - time)
			return res.send(result);

		}catch(error){
			if (!error.statusCode) {
                error.statusCode = 500;
            }
            next(error);
        }
	},

	queryInMetaData: async (req, res, next) => {
		try {
			let key = req.params.key;
 			console.log(key)
			const errors = validationResult(req);
			if (!errors.isEmpty()) {
                let error = errors.errors
				let object = {
					"status" : 500,
					error
				}
				return res.status(200).send({object})
            }

			var result = await queryService.queryInMetaData(key);
			return res.send(result);

		}catch(error){
			if (!error.statusCode) {
                error.statusCode = 500;
            }
            next(error);
        }
	},

	createExMetaData: async (req, res, next) => {
		console.log("vao day")
		try {
			start = new Date().getTime() / 1000
			let src = req.body.org_src;
			let to = req.body.org_dest;
			let fromUser = req.body.user_from;
			let toUser = req.body.user_to;
			let cid = req.body.cid;
 			

			const errors = validationResult(req);
			if (!errors.isEmpty()) {
                let error = errors.errors
				let object = {
					"status" : 500,
					error
				}
				return res.status(200).send({object})
            }

            var key = to + toUser + cid
			var result = await invokeService.createExMetaData(key, src, to, fromUser, cid, toUser);
			end = new Date().getTime() / 1000

			console.log(start - end)


			return res.send(result);

		}catch(error){
			if (!error.statusCode) {
                error.statusCode = 500;
            }
            next(error);
        }
	},

	queryExMetaData: async (req, res, next) => {
		try {
			let key = req.params.key;
 			console.log("day la ",key)
			const errors = validationResult(req);
			if (!errors.isEmpty()) {
                let error = errors.errors
				let object = {
					"status" : 500,
					error
				}
				return res.status(200).send({object})
            }

			var result = await queryService.queryExMetaData(key);
			return res.send(result);

		}catch(error){
			if (!error.statusCode) {
                error.statusCode = 500;
            }
            next(error);
        }
	}
})





























