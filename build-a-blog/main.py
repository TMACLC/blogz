from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
                                    
class Blog(db.Model):
                                  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text) 
    post = db.Column(db.Text)   

    def __init__(self, title, post):
        self.title = title
        self.post = post 


@app.route("/blog")
def blog():
    post_id = request.args.get('id')
    if (post_id):
        ind_post = Blog.query.get(post_id)
        return render_template('ind_post.html', ind_post=ind_post)
    else:
       
       
        all_blog_posts = Blog.query.all()
        
        return render_template('blog.html', posts=all_blog_posts)



def empty(v):
    if v:
        return True
    else:
        return False    

   
  



@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():
    if request.method =='POST':

        

        title_error = ""
        blog_entry_error = ""

        
        post_title = request.form['blog_title']
        post_entry = request.form['blog_post'] 
        new_post = Blog(post_title, post_entry)
    
        if empty(post_title) and empty(post_entry):
            db.session.add(new_post)
            db.session.commit()
            post_link = "/blog?id" + str(new_post.id)
            return redirect(post_link)
        
        else:
            if not empty(post_title) and not empty(post_entry):
                title_error = "You must enter a title" 
                blog_entry_error = "You must write a blog entry"
                return render_template('new_post.html', blog_entry_error = blog_entry_error,title_error = title_error)
            elif not empty(post_title):
                title_error = "You must enter a title"
                return render_template('new_post.html', title_error = title_error, post_entry = post_entry)
            elif not empty(post_entry):
                blog_entry_error = "You must write a blog entry"
                return render_template('new_post.html', blog_entry_error = blog_entry_error,post_title = post_title)
                
 

    else:
        return render_template('new_post.html')
    
 



if __name__ == '__main__':
    app.run()