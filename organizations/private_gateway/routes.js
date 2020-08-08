var controller = require('./controller');
const express 				= require('express');
const router 				= express.Router();

// 
router.post('/api/push/data/internal/blockchain', controller.createInMetaData)

// bawsn data tu eth to smartcontrac
router.post('/api/push/data/external/blockchain', controller.createExMetaData)

router.get('/api/get/data/internal/:key', controller.queryInMetaData)
router.get('/api/get/data/external/:key', controller.queryExMetaData)


module.exports = router;