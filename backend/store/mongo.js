const mongoose = require('mongoose');

const config = require('../config');
const { response } = require('express');

const configdb = {
    url: config.mongo.url
}

function indicateDB() {
    mongoose.connect(configdb.url, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    })
    .then(() => {
        console.log('DB connected')
    })
    .catch(err => {
        if (err) {
            console.error('[db err]', err), '1';
            setTimeout(indicateDB(), 2000);
        }
    })
}

function handleConnection() {
    indicateDB()
    const db = mongoose.connection
    db.on('error', err => {
        console.error('[db err]', err);
        if (err.code === 'ESERVFAIL') {
            setTimeout(handleConnection(), 2000);
        }  else {
            throw err
        }
    })
    db.once('open', function () {
        console.log('Conect sucesfull');
    })
}

handleConnection()

const Schema = mongoose.Schema;

const schemas = {

    productSchema: new Schema({
        productName: {type: String},
        imageUrl: {type: String},
        productUrl: {type: String},
        price: {type: Number},
        stars: {type: Number},
        reviews: {type: Number},
        rank: {type: Number},
        /*↓↓Working↓↓ */
        // time: {type: Date}
    }, {collection: 'Products'}),
    storeSchema: new Schema({
        Name: {type: String},
        price: {type: Number},
        stars: {type: Number},
        reviews: {type: Number},
        rank: {type: Number},
        /*↓↓Working↓↓ */
        // time: {type: Date}
    }, {collection: 'Stores'}),
    cathegorySchema: new Schema({
        productName: {type: String},
        imageUrl: {type: String},
        productUrl: {type: String},
        price: {type: Number},
        stars: {type: Number},
        reviews: {type: Number},
        rank: {type: Number},
        /*↓↓Working↓↓ */
        // time: {type: Date}
    }, {collection: 'Cathegorys'}),
    countrySchema: new Schema({
        productName: {type: String},
        imageUrl: {type: String},
        productUrl: {type: String},
        price: {type: Number},
        stars: {type: Number},
        reviews: {type: Number},
        rank: {type: Number},
        /*↓↓Working↓↓ */
        // time: {type: Date}
    }, {collection: 'Countrys'}),

    
};

const productsSchema = schemas.productSchema;
const storesSchema = schemas.storeSchema;
const cathegorysSchema = schemas.cathegorySchema;
const countrysSchema = schemas.countrySchema;

const models = {
    
    Products: mongoose.model('Products', productsSchema),
    Stores: mongoose.model('Stores', storesSchema),
    Cathegorys: mongoose.model('Cathegorys', cathegorysSchema),
    Countrys: mongoose.model('Countrys', countrysSchema)
    
};

const Products = models.Products
const Stores = models.Stores
const Cathegorys = models.Cathegorys
const Countrys = models.Countrys

const selectColllection = (schema) => {
    switch (schema) {
        case 'Products':
            return Products
        case 'Stores':
            return Stores
        case 'Cathegorys':
            return Cathegorys
        case 'Countrys':
            return Countrys
    
        default:
            break;
    }
}

function list(schema, data) {
    const collection = selectColllection(schema)
    let query = {}
    if (data) {
        query = {'countryID' : `${data._id}`}
    }
    return collection.find(query)
}

function get(schema, id) {
    const collection = selectColllection(schema)
    return collection.find({ '_id': `${id}`})
}

module.exports = {
    list,
    get
}