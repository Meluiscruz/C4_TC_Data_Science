const express = require('express')
const bodyParser = require('body-parser')

const swaggerUI = require('swagger-ui-express')

const config = require('../config')

const app = express()

app.use(bodyParser.json())

const swaggerDoc = require('./swagger.json')

//Router

app.use('/api-docs/v1', swaggerUI.serve, swaggerUI.setup(swaggerDoc))

app.listen(config.api.port, () => {
    console.log('Api escuchando en el puerto', config.api.port);
})