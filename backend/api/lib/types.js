'use strict'

const connectDB = require('./db')
const { ObjectID } = require('mongodb')
const errorHandler = require('./errorHandler')


module.exports = {
    Product: {
        store: async ({ store }) => {
            let db
            let Data
            try {
                db = await connectDB()
                Data = await db.collection('Stores').findOne({_id: ObjectID(store)})
            } catch (e) {
                errorHandler(e)
            }

            return Data
        },
        cathegory: async ({ cathegory }) => {
            let db
            let Data
            try {
                db = await connectDB()
                Data = await db.collection('Cathegorys').findOne({_id: ObjectID(cathegory)})
            } catch (e) {
                errorHandler(e)
            }

            return Data
        }, 
        country: async ({ country }) => {
            let db
            let Data
            try {
                db = await connectDB()
                Data = await db.collection('Countrys').findOne({_id: ObjectID(country)})
            } catch (e) {
                errorHandler(e)
            }

            return Data
        } 
    },
    GlobalSearch: {
        __resolveType: (item, context, info) => {
            return 'Product'
        }
    }
}