from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#connection to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
#helps debug
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'tmaccodes2019'


                                    
class Blog(db.Model):
    #specify data that goes into columns                              
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text) 
    post = db.Column(db.Text)

    #foreign key linking user's id to the blog post
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#see Get it done, constructor set up 
    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner =owner 

#creating a user class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique = True)
    password = db.Column(db.String(100))
    blogs = db.relationship('Blog', backref ='owner')
     # signifies a relationship between the blog table  user, binding this user 
    #with the blog posts they write.

    def __init__(self,username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    #endpoint is the name of the view function, not the url path.
    allowed_routes = ['list_blogs', 'add_user','user_login']

    # if not in list, and user not logged in, it will redirect to login page
    if request.endpoint not in allowed_routes and 'username' not in session:

        return redirect('/login')

@app.route('/')
def index():
    all_users = User.query.distinct()
    return render_template('index.html', list_all_users=all_users)





@app.route("/blog")
def list_blogs():
    post_id = request.args.get('id')
    single_user_id = request.args.get('owner_id')
    if (post_id):
        ind_post = Blog.query.get(post_id)
        return render_template('ind_post.html', ind_post=ind_post)
    else:
        if (single_user_id):
            ind_user_blog_posts = Blog.query.filter_by(owner_id=single_user_id)
            return render_template('singleUser.html', posts=ind_user_blog_posts)
        else:
# search db for all entries
            all_blog_posts = Blog.query.all()
        
            return render_template('blog.html', posts=all_blog_posts)



def empty(v):
    if v:
        return True
    else:
        return False    

   
  

#updated:/newpost route handler function with new parameter when creating new blog entry.

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():
    if request.method =='POST':

        

       # title_error = ""
        #blog_entry_error = ""

        #blog title,blog post frm entry form
        post_title = request.form['blog_title']
        post_entry = request.form['blog_post'] 
        #assign owner frm user signup
        owner = User.query.filter_by(username=session['username']).first()
        #from title&entry
        new_post = Blog(post_title, post_entry,owner)
    
        if empty(post_title) and empty(post_entry):
            db.session.add(new_post)
            db.session.commit()
            post_link = '/blog?id=' + str(new_post.id)
            return redirect(post_link)
        
        else:
            if not empty(post_title) and not empty(post_entry):

                #title_error = "You must enter a title" 
                #blog_entry_error = "You must write a blog entry"
                flash('You must enter a title and a blog entry') 
            elif not empty(post_title):
                #using flash,dont need this statement,blog_entry_error = blog_entry_error,title_error = title_error 
                return render_template(post_title = post_title)
            elif not empty(post_title):
                flash('You must enter a title')
                return render_template('new_post.html', post_entry = post_entry)
            elif not empty(post_entry):
                flash("You must write a blog entry")
                return render_template('new_post.html', post_title = post_title)
                
 

    else:
        return render_template('new_post.html')

#see The code from Get It Done.& User Signup for validation tasks.
@app.route('/signup', methods = ['POST', 'GET'] ) 
def add_user():
    if request.method =='POST':

        #variable assignments, signup.html

        user_name = request.form['username']
        user_password = request.form['password']
        user_password_validate = request.form['password_validate']
        existing_user = User.query.filter_by(username = user_name).first()

#use cases
        if not empty(user_name) or not empty (user_password) or not empty (user_password_validate):
            flash('one or more fields are blank or invalid')
            return render_template('signup.html')

        if user_password != user_password_validate:
            flash('Passwords must match')
            return render_template('signup.html')

        if len(user_password) <3 and  len(user_name) < 3:
            flash('Username must be at least 3 characters long')
            return render_template('signup.html')

        if len(user_password) <3:
            flash('Password must be at least 3 characters long') 
            return render_template('signup.html')

        if len(user_name) < 3:
            flash('Username must be at least three characters')
            return render_template('signup.html')    

        #existing_user = User.query.filter_by(username = user_name).first()
    

        if not existing_user:

            new_user = User(user_name, user_password)

            db.session.add(new_user)

            db.session.commit()

            session['username'] = user_name

            flash('Welcome, New user created')

            return redirect('/newpost')
        else: 
            flash('That username already exists') 
            return render_template('signup.html')

    else: 
        return render_template('signup.html') 

@app.route('/login', methods = ['POST', 'GET'])
def user_login(): 

   # if request.method == 'GET':
        #return render_template("login.html")

    if request.method == 'POST':

        #variable assignement, login.html

        username = request.form['username']
        password = request.form['password']
        #search db for unique username
        user = User.query.filter_by(username=username).first()


        #use cases/conditionals

        if not username and not password:
            #flash('Username or password fields must not be blank')
            return render_template('login.html')
        if not username :
            #flash('Username is blank Please enter something.')
            return render_template('login.html')
        if not password:
            #flash('Password is blank Please enter something.')
            return render_template('login.html')     

       # user = User.query.filter_by(username=username).first()    

        if not user:
            #flash('Username does not exist')
            return render_template('login.html')
        if user.password != password:
            #flash('Password is wrong')
            return render_template('login.html') 
        
        if user and user.password==password:
            session['username'] = username
            return redirect('/newpost')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    #flash('You are logged out')
    return redirect('/blog')
 

#when main.py runs,

if __name__ == '__main__':
    app.run()