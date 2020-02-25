from ariadne import gql, QueryType, graphql_sync, make_executable_schema,MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

type_defs = gql("""#the gql validate schema and raises error
    type Query {
        hello: String!
        test(name: String): String!
        all: [String]!
    }
    type Mutation{
        add(name: String!): String!
    }
""")

users = ["Unknown"]

query = QueryType()


@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent


@query.field("test")
def resolve_test(*_, name=users[-1]):
    return "Hello, %s" % name

@query.field("all")
def resolve_all(*_):
    return users

mutation = MutationType()

@mutation.field("add")
def resolve_add(_,info,name):
    users.append(name)
    return users[-1]

schema = make_executable_schema(type_defs, query, mutation)

app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
