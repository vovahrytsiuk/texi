from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from Handler import *
from SingletonDB import DB

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    facade = Facade()

    query = ObjectType("Query")
    query.set_field("listRequests", facade.requests_resolver)

    type_defs = load_schema_from_path("schema.graphql")
    schema = make_executable_schema(
        type_defs, query, snake_case_fallback_resolvers
    )


    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200


    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code

    @app.route("/get_requests/", methods=['GET', 'POST', 'DELETE', 'PUT'])
    def get_requests():
        post = Post()
        get = Get()
        delete = Delete()
        put = Put()
        post.set_next(get).set_next(delete).set_next(put)
        return post.handle(request.method)

    app.run(debug=False)
    DB().conn.close()

