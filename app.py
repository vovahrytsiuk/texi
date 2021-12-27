from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from Handler import *
from SingletonDB import DB

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    @app.route("/get_requests/", methods=['GET', 'POST', 'DELETE', 'PUT'])
    def get_prod():
        post = Post()
        get = Get()
        delete = Delete()
        post.set_next(get).set_next(delete)
        return post.handle(request.method)

    app.run(debug=True)
    DB().conn.close()

