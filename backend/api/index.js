const { makeExecutableSchema } = require('graphql-tools')
const express = require("express");
const { graphqlHTTP } = require("express-graphql");
const cors = require("cors");
const { readFileSync } = require("fs");
const { join } = require("path");
const resolvers = require("./lib/resolvers");
const config = require("../config");

const app = express();
const port = process.env.PORT || 3000;

// definiendo el schema
const typeDefs = readFileSync(
  join(__dirname, "lib", "schema.graphql"),
  "utf-8"
);

const schema = makeExecutableSchema({typeDefs, resolvers});

app.use(cors());

app.use(
  "/api",
  graphqlHTTP({
    schema: schema,
    rootValue: resolvers,
    graphiql: false,
  })
);

app.use(
  "/api-docs/v2",
  graphqlHTTP({
    schema: schema,
    rootValue: resolvers,
    graphiql: true,
  })
);

app.listen(port, () => {
  console.log(`Server is listening at http://localhost:${config.api.port}/api`);
});
