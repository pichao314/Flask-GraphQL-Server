# cmpe273-lab3
Implementation of GraphQL

## Instruction

- The "myapp.py" contains the server implementation
- The "schema.graphql" contains the schema definition
- Place these two file in same directory to make the path available

## Result

### Operation of students

- Add a student

```python
#request
mutation{
	student(name: "PC")
}

#response
{
  "data": {
    "student": true
  }
}
```

- Request all students
  
```python
#request
{
  students{
    id
    name
  }
}

#response
{
  "data": {
    "students": [
      {
        "id": 1,
        "name": "chao"
      },
      {
        "id": 2,
        "name": "PC"
      }
    ]
  }
}
```

### Operation of Class

- Add a class

```python
#request
mutation{
  class(id:272, name:"Software Platform")
}

#response
{
  "data": {
    "class": true
  }
}
```

- Request all class

```python
#request
{
  classes{
    id
    name
    students{
      name
    }
  }
}

#response
{
  "data": {
    "classes": [
      {
        "id": 273,
        "name": "Distributed System",
        "students": []
      },
      {
        "id": 272,
        "name": "Software Platform",
        "students": []
      }
    ]
  }
}
```

- Add a student into class

```python
#request
mutation{
  add(sid:1,cid:272)
}

#response
{
  "data": {
    "add": true
  }
}
```

- Request a class

```python
#request
{
  class(id: 272){
    id
    name
    students{
      id
      name
    }
  }
}

#response
{
  "data": {
    "class": {
      "id": 272,
      "name": "Software Platform",
      "students": [
        {
          "id": 1,
          "name": "chao"
        }
      ]
    }
  }
}
```

## Pre-requisites

* Install _Pipenv_

```
pip install pipenv
```

* Install _[Flask](https://palletsprojects.com/p/flask/)_

```
pipenv install flask==1.1.1
```
* Install _[Graphene](https://graphene-python.org/)_ and [Flask GraphQL](https://github.com/graphql-python/flask-graphql) for handling GraphQL schema and binding.

```
pipenv install graphene==2.1.8
pipenv install flask-graphql==2.0.1
```

* Create a schema.py and add this code:

```python
from graphene import ObjectType, String, Boolean, ID, Field, Int, List


class Student(ObjectType):
    id = ID()
    name = String()

# List view of <any> objects
class Query(ObjectType):
    students = List(Student, id=Int(required=True))

    def resolve_students(self, args, context, info):
        students = [ { "name": "fix" }, { "name": "me" }]
        return students

schema = graphene.Schema(query=Query)

def test():
    query = '''
        query students {
            name
        }
    '''
    result = schema.execute(query)
    print(f"result={result}")
```

* Create a file called _app.py_ and add this code snippet.

```python
from flask import Flask, escape, request
from schema import Query
from flask_graphql import GraphQLView
from graphene import Schema

view_func = GraphQLView.as_view(
    'graphql', schema=Schema(query=Query), graphiql=True)


app = Flask(__name__)
app.add_url_rule('/graphql', view_func=view_func)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
```

* Run your Hello World Flask application from a shell/terminal.

```sh
pipenv shell
$ env FLASK_APP=app.py flask run
```

* Open [this URL](http://127.0.0.1:5000/) in a web browser or run this CLI to see the output.

```
curl -i http://127.0.0.1:5000/
```

## Requirements

You will be building a RESTful class registration API in this lab.

### Domain Model

```
|-------|               |---------|
| Class |* ---------- * | Student |
|-------|               |---------|
```

### GraphQL operations to be implemented.

* Mutate a new student

```
{
    "name": "Bob Smith"
}
```

* Quety an existing student

_Request_

```
{
  students(id:1238125) {
    name
  }
}
```

_Response_

```
{
    "name" : "Bob Smith"
}
```

* Mutate a class

```
TBD
```

* Query a class

```
{
  classess(id:1238125) {
    name
    students
  }
}
```

* Add students to a class

```
TBD
```

