from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse

from Handler import  Put, Post, Delete, Get
from SingletonDB import DB
from CacheData import CacheTable

if __name__ == "__main__":

    app = Flask(__name__)
    api = Api(app)
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

