const store = require('../../../store/mongo')
const controller = require('./controller')

module.exports = controller(store)