import peewee as pw
# ----------------------------------------------------------------------
# Models:
# ----------------------------------------------------------------------
DB_NAME = 'jlog'
DB_USER = 'javad'
DB_PSSWD = '156725'
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
DB_Check_Author = DB.execute_sql("SHOW TABLES LIKE 'Author'").fetchone()
if str(DB_Check_Author) == "None":
    print("Table is non-existent, Creating Author")
    DB.create_table(Author)
else:
    print("initializing Author...")

DB_Check_Post = DB.execute_sql("SHOW TABLES LIKE 'Post'").fetchone()
if str(DB_Check_Post) == "None":
    DB.create_table(Post)
    print("Table is non-existent, Creating Post")
else:
    print("initializing Post...")

DB_Check_Blog = DB.execute_sql("SHOW TABLES LIKE 'Blog'").fetchone()
if str(DB_Check_Blog) == "None":
    print("Table is non-existent, Creating Blog")
    DB.create_table(Blog)
else:
    print("initializing Blog...")
