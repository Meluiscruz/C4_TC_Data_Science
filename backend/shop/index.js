const express = require('express')
const bodyParser = require('body-parser')

const config = require('../config')
const shop = require('./components/shop/network')
const errors = require('../network/errors')

const app = express()

app.use(bodyParser.json())

//Router

app.use('/api/shop', shop)

app.use(errors )

app.listen(config.shop.port, () => {
    console.log('Shop escuchando en el puerto ', config.shop.port)
})