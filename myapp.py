from ariadne import gql, QueryType, ObjectType, graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify


type_defs = load_schema_from_path("./schema.graphql")

query = ObjectType("Query")

st = [
    {
        'id': 1,
        'name': "chao"
    }
]

cl = [
    {
        'id': 273,
        'name': "Distributed System",
        'students': []
    }
]


@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent


@query.field("students")
def resolve_students(obj, info):
    return st


@query.field("student")
def resolve_student(obj, info, id):
    for each in st:
        if each['id'] == id:
            return each
    return None


@query.field("classes")
def resolve_classes(obj, info):
    return cl


@query.field("class")
def resolve_classes(obj, info, id):
    for each in cl:
        if each['id'] == id:
            return each
    return None


mutation = ObjectType("Mutation")


@mutation.field("student")
def resolve_m_student(obj, info, name):
    st.append(
        {
            'id': len(st)+1,
            'name': name
        }
    )
    return True


@mutation.field("class")
def resolve_m_class(obj, info, id, name):
    for each in cl:
        if each["id"] == id:
            return False
    cl.append(
        {
            'id': id,
            'name': name,
            'students': []
        }
    )
    return True


@mutation.field("add")
def resolve_add(obj, info, sid, cid):
    for s in st:
        if s['id'] == sid:
            for c in cl:
                if c['id'] == cid:
                    for cs in c['students']:
                        if cs['id'] == sid:
                            return False
                    c['students'].append(s)
                    return True
            return False
    return False


student = ObjectType("Student")


@student.field("id")
def resolve_students_id(obj, info):
    return obj['id']


@student.field("name")
def resolve_students_name(obj, info):
    return obj['name']


schema = make_executable_schema(type_defs, query, mutation, student)

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
