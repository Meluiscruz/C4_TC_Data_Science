const express = require('express')
const bodyParser = require('body-parser')

const config = require('../config')
const cathegory = require('./components/cathegory/network')
const errors = require('../network/errors')

const app = express()

app.use(bodyParser.json())

//Router

app.use('/api/cathegory', cathegory)

app.use(errors )

app.listen(config.cathegory.port, () => {
    console.log('cathegory escuchando en el puerto ', config.cathegory.port)
})