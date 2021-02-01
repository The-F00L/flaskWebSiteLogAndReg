from flask import Flask,session,render_template,request,redirect,g,url_for,flash
import datetime
import os
import hashlib

app = Flask(__name__)

app.secret_key=os.urandom(24)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        session.pop('user',None)
        #modify later
        #without database testing
        if passVal(str(request.form['password'])).digest()==passVal("password").digest() and request.form['username']=='admin' :
            session['user']=request.form['username']
            return redirect(url_for('protected'))
    return render_template('index.html')

@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html',user=session['user'])
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('reg.html')
    if request.method=='POST':
        if request.form['password']==request.form['password-repeat']:
            #adatabazisba
            return redirect(url_for('regSucces'))
        else:
            return redirect(url_for('regUN'))
    return render_template('reg.html')

@app.route('/regUN')
def regUN():
    return render_template('regUN.html')

@app.route('/regSucces')
def regSucces():
    return render_template('succesReg.html')


@app.route('/dropsession')
def dropsession():
    session.pop('user',None)
    return render_template('index.html')

#sozos hash db store
#so=name+pass
#so=len(name)
# or wha???
#

def passVal(password):
    return hashlib.md5(password.encode())

if __name__=='__main__':
    app.run(debug=True)