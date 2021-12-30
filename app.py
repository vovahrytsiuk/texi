from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse

from Handler import Put, Post, Delete, Get
from SingletonDB import DB
from CacheData import CacheTable

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from Facade import Facade


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    facade = Facade()

    query = ObjectType("Query")
    mutation = ObjectType("Mutation")

    query.set_field("listRequests", facade.requests_resolver)
    query.set_field("listClients", facade.clients_resolver)
    query.set_field("listDrivers", facade.driver_resolver)
    query.set_field("listOperators", facade.operator_resolver)

    mutation.set_field("createDriver", facade.create_driver_resolver)
    mutation.set_field("createClient", facade.create_client_resolver)
    mutation.set_field("createOperator", facade.create_operator_resolver)
    mutation.set_field("createRequest", facade.create_request_resolver)
    mutation.set_field("updateClient", facade.update_client_resolver)
    mutation.set_field("updateDriver", facade.update_driver_resolver)
    mutation.set_field("updateOperator", facade.update_operator_resolver)
    mutation.set_field("deleteClient", facade.delete_client_resolver)
    mutation.set_field("deleteDriver", facade.delete_driver_resolver)

    type_defs = load_schema_from_path("schema.graphql")
    schema = make_executable_schema(
        type_defs, query, mutation, snake_case_fallback_resolvers
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

    app.run(debug=True)
    DB().conn.close()

