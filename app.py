import sys
sys.path.insert(0,'db/')
from db.dbhelper import *

from flask import Flask,render_template,request,redirect,session,flash

app = Flask(__name__)
app.config['SECRET_KEY']='d71068e934814ce781d1cfe5c3090684'

@app.route("/")
def index()->None:
    return render_template('index.html')
    
@app.route("/loginvalidate",methods=['POST'])
def loginvalidate()->None:
    username:str = request.form['username']
    password:str = request.form['password']
    user:list = getrecord('users',username=username,password=password)
    if len(user)>0:
        session['username'] = username
        return redirect("/main")
    else:
        flash('Bad username and password','error')
        return redirect("/")
    #routename:str = "/main" if len(user)>0 else "/"
    #return redirect(routename)
    
@app.route("/saveuser",methods=['POST'])
def saveuser()->None:
    username:str = request.form['username']
    password:str = request.form['password']
    type:str = request.form['type']
    id:str = request.form['id']
    print(id)
    print(username)
    print(password)
    if type=='add':
        ok:bool = addrecord('users',username=username,password=password)
    else:
        ok:bool = updaterecord('users',id=id,username=username,password=password)
    
    if ok==True:
        flash("User Information Saved","info")
    else:
        flash("Error Saving User information","error")
    return redirect("/main")
    
@app.route("/deleteuser")
def deleteuser()->None:
    id:int = request.args.get('id')
    ok:bool = deleterecord('users',id=id)
    if ok==True:
        flash("User Deleted","success")
    else:
        flash("Error Deleting User","error")
    return redirect("/main")
    
        
@app.route("/main")
def main()->None:
    if 'username' in session:
        users:list = getall('users')
        return render_template('main.html',userlist=users)
    else:
        flash('Log in Properly','info')
        return redirect("/")

@app.route('/logout')
def logout():
    session.pop('username', None) # Remove 'username' from session
    flash('You are logged out','info')
    return redirect("/")
    

    
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__=="__main__":
    app.run(debug=True)