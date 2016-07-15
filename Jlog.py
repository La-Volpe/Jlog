from flask import Flask
from flask_restful import Resource, Api, reqparse
from datetime import datetime
import Models as m

app = Flask(__name__)
api = Api(app)
# ----------------------------------------------------------------------
# Controllers:
# ----------------------------------------------------------------------
class SubmitPost(Resource):
    """Submits a post and stores it inside a database"""
    def post(self):
        try:
            #Parsing the request
            parser = reqparse.RequestParser()
            print('passed parser')
            parser.add_argument('title')
            parser.add_argument('author')
            parser.add_argument('text')
            args = parser.parse_args()
            print(args)
            #Storing the post in database
            new_post = m.Post(author=args['author'],
                              title=args['title'],
                              text=args['text'],
                              date=str(datetime.now())
                              )
            print(datetime.now())
            new_post.save()
            return {'Success':200}
        except Exception as e:
            print(str(e))
            return {'error': str(e)}


class ShowPost(Resource):
    """Shows a certain post, with the given ID. Posts are stored
    in a LIFO order, the most recent entry's ID is always 1,
    and the last one is equal to the number of posts...
    """
        # With Post ID
    def get(self,id):
        try:

            try:
                query = m.Post.select().where(m.Post.id == id).get()
            except Exception as e:
                return {'error':'Something went wrong! The post is probably non-existent!'}
            post = \
                {
                'id': query.id,
                'title': query.title,
                'author': query.author,
                'text': query.text,
                'date': str(query.date)
                }
            print(post)
            return post

        except Exception as e:
            print(str(e))
            return {'error': str(e)}


class ShowPosts(Resource):
    # Showing All the posts! Yay!
    def get(self):
        try:
            Posts = []
            for _post in m.Post.select().order_by(m.Post.date.desc()):
                Posts.append(
                    {
                        'id': _post.id,
                        'title': _post.title,
                        'author': _post.author,
                        'text': _post.text,
                        'date': str(_post.date)
                    }
                )
            print(Posts)
            return Posts

        except Exception as e:
            print(str(e))
            return {'error': str(e)}


class DeletePost(Resource):
    def get(self,id):
        post = m.Post.select().where(m.Post.id == id).get()
        post.delete_instance()
        return {200:'Post deleted'}

api.add_resource(SubmitPost,'/submit')
api.add_resource(ShowPosts,'/show/', '/show')
api.add_resource(ShowPost,'/show/<int:id>')
api.add_resource(DeletePost,'/delete/<int:id>')
if __name__ == '__main__':
    app.run(debug=True)
