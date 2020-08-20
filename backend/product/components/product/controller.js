const SCHEMA =  'Products'

module.exports = function (injectedStore) {
    let store = injectedStore

    if(!store) console.error('Db undifined');

    async function list() {
        return await store.list(SCHEMA)
    }

    function get (id) {
        data = store.get(SCHEMA, id)
        return data
    }

    return {
        list,
        get
    }
}
