const express = require('express')
const bodyParser = require('body-parser')

const config = require('../config')
const product = require('./components/product/network')
const errors = require('../network/errors')

const app = express()

app.use(bodyParser.json())

//Router

app.use('/api/product', product)

app.use(errors )

app.listen(config.product.port, () => {
    console.log('Product escuchando en el puerto ', config.product.port)
})