import os
import flask
from flask import Flask
from flask_restful import Api, Resource, abort, fields, marshal_with
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
# Creating an app for Flask
app = Flask(__name__)
# Wrapping the app with an API
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes}"



video_put_args = reqparse.RequestParser()

video_put_args.add_argument("name", type=str, help="Name of the video required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video required")
video_update_args.add_argument("views", type=int, help="Views of the video required")
video_update_args.add_argument("likes", type=int, help="Likes of the video required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer

}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(409, message="couldn't find Video")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message = "Video taken")
        video = VideoModel(id=video_id, name =args['name'], views = args['views'],
                           likes = args['likes'])
        db.session.add((video))
        db.session.commit()
        return video, 201  # 201 means created and 200 means nothing broke

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(409, message="couldn't find Video")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result

    def delete(self, video_id):
        return '', 204  # deleted


api.add_resource(Video, "/video/<int:video_id>")



# Starting our server and application
if __name__ == "__main__":
    app.run(debug=True)
