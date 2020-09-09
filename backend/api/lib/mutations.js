const connectDB = require('./db')
const { ObjectID } = require('mongodb')
const errorHandler = require('./errorHandler')

module.exports = {
    releaseProduct: async (root, { input }) => {
        
        //nuevo objeto
        const newProduct = Object.assign(input)

        let db
        let product
        let condition

        try {

            db = await connectDB()
            condition = await db.collection('Products').findOne({link: newProduct.link})
            
            if(condition) {

                await db.collection('Products').updateOne(
                    { _id: ObjectID(condition._id)  },
                    {$set: newProduct}
                )

                Product = await db.collection('Products').findOne({_id: ObjectID(condition._id)})

            } else {

                //Verifica si existe en categorias
                //si es asi le añade el ID sino la crea y añade el id
                exist = await db.collection('Cathegorys').findOne({name: newProduct.cathegory})
                if(exist) {
                    newProduct.cathegory = ObjectID(exist._id) 
                } else {
                    await db.collection('Cathegorys').insertOne({name: newProduct.cathegory}) 
                }

                //Verifica si existe la tienda
                //si es asi le añade el ID sino la crea y añade el id
                exist = await db.collection('Stores').findOne({name: newProduct.store})
                if(exist) {
                    newProduct.store = ObjectID(exist._id) 
                } else {
                    await db.collection('Stores').insertOne({name: newProduct.store}) 
                }
                
                //Verifica si existe el pais
                //si es asi le añade el ID sino la crea y añade el id
                exist = await db.collection('Countrys').findOne({country: newProduct.country})
                if(exist) {
                    newProduct.country = ObjectID(exist._id) 
                } else {
                    await db.collection('Countrys').insertOne({country: newProduct.country}) 
                }
                Product = await db.collection('Products').insertOne(newProduct)
                Product = db.collection('Products').findOne({_id: ObjectID(Product.insertedId)})
            }
        } catch (e) {
            errorHandler(e)
        }

        return Product
    },
    // createPerson: async (root, { input }) => {
    //     let db
    //     let student
    //     try {
    //         db = await connectDB()
    //         student = await db.collection('students').insertOne(input)
    //         input._id = student.insertedId
    //     } catch (e) {
    //         errorHandler(e)
    //     }

    //     return input
    // },
    // editCourse: async (root, { _id, input }) => {
    //     let db
    //     let course
    //     try {
    //         db = await connectDB()
    //         await db.collection('courses').updateOne(
    //             {_id: ObjectID(_id)},
    //             {$set: input}
    //         )
    //         course = await db.collection('courses').findOne({_id: ObjectID(_id)})
    //     } catch (e) {
    //         errorHandler(e)
    //     }

    //     return course
    // },
    // editPerson: async (root, { _id, input }) => {
    //     let db
    //     let student
    //     try {
    //         db = await connectDB()
    //         await db.collection('students').updateOne(
    //             {_id: ObjectID(_id)},
    //             {$set: input}
    //         )
    //         student = await db.collection('students').findOne({_id: ObjectID(_id)})
    //     } catch (e) {
    //         errorHandler(e)
    //     }

    //     return student
    // },
    // deleteCourse: async (root, { _id }) => {
    //     let db
    //     let info
    //     try {
    //         db = await connectDB()
    //         info = await db.collection('courses').deleteOne({_id: ObjectID(_id)})
    //     } catch (e) {
    //         errorHandler(e)
    //     }

    //     return info.deletedCount ? `El curso id: ${_id} fue eliminado` : `No existe el curso indicado`
    // },
    // deletePerson: async (root, { _id }) => {
    //     let db
    //     let info
    //     try {
    //         db = await connectDB()
    //         info = await db.collection('students').deleteOne({_id: ObjectID(_id)})
    //     } catch (e) {
    //         errorHandler(e)
    //     }
        
    //     return info.deletedCount ? `El estudiante id: ${_id} fue eliminado` : `No existe el curso indicado`
    // },
    // addPeople: async (root, {courseID, personID}) => {
    //     let db
    //     let person
    //     let course
    //     try {
    //         db = await connectDB()
    //         course = await db.collection('courses').findOne({_id: ObjectID(courseID)})
    //         person = await db.collection('students').findOne({_id: ObjectID(personID)})
    //         if (!course || !person) throw new Error('La persona o el curso no existe')

    //         await db.collection('courses').updateOne(
    //             { _id: ObjectID(courseID)  },
    //             { $addToSet: {people: ObjectID(personID) } }
    //         )
    //     } catch (e) {
    //         errorHandler(e)
    //     }
    
    //     return course
    // }
}