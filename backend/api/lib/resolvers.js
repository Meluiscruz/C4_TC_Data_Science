'use strict'

// const mutation = require('./mutations')
const queries = require('./queries')
const types = require('./types')

module.exports = {
    Query: queries,
    // Mutation: mutation,
    ...types
}