from operator import pos
from typing import DefaultDict
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from sqlalchemy.orm import defaultload
from datetime import datetime
from wtforms import Form, StringField, TextAreaField, PasswordField, form, validators,SelectField,IntegerField,FormField
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from functools import wraps
from django.forms import widgets
import pycountry
from wtforms.fields.core import Label
from wtforms.fields.html5 import DateField

import pycountry
pycountry.languages 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/baris/OneDrive/Masaüstü/MSKU SENG APP/todo.db'
db = SQLAlchemy(app)

app.secret_key = "mskuseng"

account_id = 0

# Kullanıcı giriş Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:  
            return f(*args, **kwargs)
        else:
            flash('Bu sayfayı görüntülemek için lütfen giriş yapın','danger')
            return redirect(url_for('login'))
    return decorated_function

# ana sayfa
@app.route('/')
def index():
    return render_template('index.html')
# doğum günü sayfası
@app.route('/birthdaylist')
def birthdaylist():
    birthdays = User.query.all()
    return render_template('birthdaylist.html',birthdays = birthdays)

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country[0], country[1]) for country in config.countries]

class LanguageSelectField(SelectField):
    def __init__(self, *args, **kwargs):
        
        super(LanguageSelectField, self).__init__(*args, **kwargs)
        self.choices = [(language[0],language[1]) for language in config.languages]
        

# dashboard
@app.route('/dashboard',methods =['POST',"GET"])
@login_required
def dashboard():
    account_id = session['id']
    if account_id != 0:
        name_value = User.query.filter_by(id=account_id).first().name
        surname_value = User.query.filter_by(id=account_id).first().surname 
        username_value = User.query.filter_by(id=account_id).first().username
        email_value = User.query.filter_by(id=account_id).first().email
        password_value = User.query.filter_by(id=account_id).first().password
        birthday_value = User.query.filter_by(id=account_id).first().birthday
        telno_value = User.query.filter_by(id=account_id).first().telno
        education_value = User.query.filter_by(id=account_id).first().education
        section_value = User.query.filter_by(id=account_id).first().section
        country_value = User.query.filter_by(id=account_id).first().country
        language_value = User.query.filter_by(id=account_id).first().language
    if account_id == 0:
        name_value = ""
    class DashboardForm(Form):
        name = StringField("İsim",default=name_value,validators=[
                        validators.Length(min=4, max=25),validators.DataRequired(message="Lütfen bir isim belirleyin")])
        surname = StringField("Soy isim",default=surname_value,validators=[
                        validators.Length(min=4, max=25),validators.DataRequired(message="Lütfen bir soyisim belirleyin")])
        email = StringField("E-mail",default=email_value,validators=[validators.Email(message="Lütfen Geçerli bir email adresi giriniz."),validators.DataRequired(message="Lütfen bir email belirleyin")])
        telno =  StringField("Telefon numarası",default=telno_value,validators=[
                        validators.Length(min=4, max=25),validators.DataRequired(message="Lütfen bir telefon no belirleyin")])
        username = StringField("Kullanıcı adı",default=username_value,validators=[
                           validators.Length(min=5, max=35),validators.DataRequired(message="Lütfen bir kullanıcı adı belirleyin")])
        birthday = DateField("Doğum gününüz")
        education = StringField("Eğitim Bilgileri",default=education_value,validators=[
                        validators.Length(min=4, max=25),validators.DataRequired(message="Lütfen eğitim durumunuzu belirleyin")])
        section = StringField("Bölümünüz",default=section_value,validators=[
                        validators.Length(min=4, max=25),validators.DataRequired(message="Lütfen bölümünüzü belirleyin")])
        country =  CountrySelectField("Ülkeniz")
        language = LanguageSelectField("Diliniz")
    
 
    form = DashboardForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        
        if User.query.filter_by(email=form.email.data).first():
            flash("Email kullanılıyor.","danger")
            return render_template('dashboard.html',form = form)
        else:
            user.email = form.email.data
        if User.query.filter_by(telno=form.telno.data).first():
            flash("Telefon Numarası kullanılıyor.","danger")
            return render_template('dashboard.html',form = form)
        else:
            user.telno = form.telno.data
        user.username = form.username.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.birthday = form.birthday.data
        user.education = form.education.data
        user.section = form.section.data
        user.country = form.country.data
        user.language = form.language.data
        
        db.session.commit()
        
    
    
    session_refresh(form.username.data)
    return render_template('dashboard.html',form = form)

# silme
@app.route('/delete/<string:id>')
def delete(id):
    user = User.query.filter_by(id = id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('logout'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    birthday = db.Column(db.String(80))
    telno = db.Column(db.String(80))
    education = db.Column(db.String(80))
    section = db.Column(db.String(80))
    country = db.Column(db.String(80))
    language = db.Column(db.String(80))
    ozel = db.Column(db.String(80))
    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(80))
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    time = db.Column(db.String(80))
    section = db.Column(db.String(80))
    def __repr__(self):
        return '<Post %r>' % self.time

class RegisterForm(Form):
    username = StringField("Kullanıcı Adı", validators=[
                           validators.Length(min=5, max=35),validators.DataRequired(message="Lütfen bir kullanıcı adı belirleyin")])
    email = StringField("Email Adresi", validators=[validators.Email(message="Lütfen Geçerli bir email adresi giriniz."),validators.DataRequired(message="Lütfen bir email belirleyin")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname="confirm",
                           message="Parolanız uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")

class LoginForm(Form):
    username = StringField("Kullanıcı Adı", validators=[
                           validators.Length(min=5, max=35),validators.DataRequired(message="Lütfen bir kullanıcı adı belirleyin")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyin"),
    ])

class AddPostForm(Form):
    area = text = TextAreaField('Text', render_kw={"rows": 10, "cols": 11})
    
    
#session yenileme"
def session_refresh(usernameEntered):
    username = usernameEntered
    id = User.query.filter_by(username=username).first().id
    name = User.query.filter_by(username=username).first().name
    surname = User.query.filter_by(username=username).first().surname
    email = User.query.filter_by(username=username).first().email
    birthday = User.query.filter_by(username=username).first().birthday
    telno = User.query.filter_by(username=username).first().telno
    education = User.query.filter_by(username=username).first().education
    section = User.query.filter_by(username=username).first().section
    country = User.query.filter_by(username=username).first().country
    language = User.query.filter_by(username=username).first().language
    #
    session['logged_in'] = True
    session['id'] = id
    session['username'] = username
    session['name'] = name
    session['surname'] = surname
    session['email'] = email
    session['birthday'] = birthday
    session['telno'] = telno
    session['education'] = education
    session['section'] = section
    session['country'] = country
    session['language'] = language
    global account_id
    account_id = session['id']

#kayıt
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        ozel = form.confirm.data
        newUser = User(username = username,email = email, password = password,ozel = ozel)
        if User.query.filter_by(username=username).first():
            flash("Kullanıcı adı kullanılıyor..","danger")
            return render_template('register.html',form = form)
            print("sorun var kullanıcı adı")
        else:
            if User.query.filter_by(email=email).first():
                flash("Email kullanılıyor..","danger")
                return render_template('register.html',form = form)
                print("sorun var email")
            else:
                db.session.add(newUser)
                db.session.commit()
                print("kayıt oldu")
                flash("Başarıyla kayıt oldunuz.","success")
                return redirect(url_for('index'))

    else:
        print("büyük sorun")
        return render_template('register.html',form = form)

#giriş
@app.route('/login',methods = ["POST","GET"])
def login():
    
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        usernameEntered = form.username.data
        passwordEntered = (form.password.data)
        usernameFromDB = User.query.filter_by(username=usernameEntered).first().username
        passwordFromDB = User.query.filter_by(username=usernameEntered).first().password
        

        if usernameFromDB == usernameEntered:
            if sha256_crypt.verify(passwordEntered,passwordFromDB):
                flash("Başarıyla giriş yaptınız.","success")
                session_refresh(usernameEntered)
                
                
                return redirect(url_for('dashboard'))
            else:
                flash("Parolanızı yanlış girdiniz.","danger")
                return render_template("login.html",form = form)
        else:
            flash("Böyle bir kullanıcı bulunmuyor.","danger")
            return render_template("login.html",form = form)  

    return render_template("login.html",form = form)
@app.route("/addpost",methods = ["GET","POST"])
@login_required
def addpost():
    form = AddPostForm(request.form)
    if request.method == "POST" and form.validate():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        post = form.area.data
        newPost = Post(post = post,name = session['name'],surname = session['surname'],time = dt_string,section = session['section'])
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('blogs'))
    return render_template("addpost.html",form = form)

@app.route("/blogs")
def blogs():
    posts = Post.query.all()
    posts.reverse()

    return render_template("blogs.html",posts = posts)

@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı","success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)