const dotenv = require('dotenv')

dotenv.config()

module.exports = {
    api: {
        port: process.env.API_PORT
    },
    mongo: {
        port: process.env.MONGO_PORT,
        connect: process.env.MONGO_CONNECT
    }
}