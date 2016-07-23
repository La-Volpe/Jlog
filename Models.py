import peewee as pw
# ----------------------------------------------------------------------
# Models:
# ----------------------------------------------------------------------
DB_NAME = 'jlog'
DB_USER = 'root'
DB_PSSWD = 'mysqlpassword'
DB = pw.MySQLDatabase(DB_NAME, user=DB_USER, passwd=DB_PSSWD)
DB.init('jlog')
DB.connect()


class BaseModel(pw.Model):
    class Meta:
        database = DB


class Author(BaseModel):
    name = pw.CharField()
    post_count = pw.IntegerField()

    def get_author(self):
        return {'name': self.name,
                'post_count':self.post_count}


class Post(BaseModel):
    title = pw.CharField()
    author = pw.CharField()
    date = pw.DateTimeField()
    text = pw.TextField()
    #Status field: Published, Draft, Deleted
    status = pw.CharField()


class Blog(BaseModel):
    postID = pw.IntegerField(primary_key=True, unique=True)
    post = pw.ForeignKeyField(Post, null=False)
    author = pw.ForeignKeyField(Author)

#Checks if Tables Exist!
DB.create_tables([Author, Post, Blog], safe=True)
	
	

