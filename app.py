from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from Handler import *
from SingletonDB import DB

if __name__ == "__main__":
    DB().generate_random_data()
    # app = Flask(__name__)
    # api = Api(app)
    #
    # @app.route("/get_requests/", methods=['GET', 'POST', 'DELETE', 'PUT'])
    # def get_requests():
    #     post = Post()
    #     get = Get()
    #     delete = Delete()
    #     put = Put()
    #     post.set_next(get).set_next(delete).set_next(put)
    #     return post.handle(request.method)
    #
    # app.run(debug=False)
    # DB().conn.close()

