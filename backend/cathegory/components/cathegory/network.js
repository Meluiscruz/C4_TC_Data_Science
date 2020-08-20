const express = require('express')

// const secure = require('./secure')
const response = require('../../../network/response')
const Controller = require('./index.js')

const router = express.Router()

//ROUTES
router.get('/', list)
// router.get('/:store', list)
router.get('/:id', get)

//functions
function list(req, res, next) {
    Controller.list(req.params.country)
    .then(data => {
        response.success(req, res, data, 200)
    })
    .catch(next)
}

function get(req, res, next) {
    Controller.get(req.params.id)
    .then((post) => {
        response.success(req, res, post, 200)
    })
    .catch(next)
}

module.exports = router