const dotenv = require('dotenv')

dotenv.config()

module.exports = {
    api: {
        port: process.env.API_PORT
    },
    mongo: {
        port: process.env.MONGO_PORT,
        url: process.env.MONGO_URL
    },
    product: {
        port: process.env.PRODUCT_PORT
    },
    shop: {
        port: process.env.SHOP_PORT
    },
    cathegory: {
        port: process.env.CATHEGORY_PORT
    }
}