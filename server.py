from flask import Flask, render_template, flash, redirect, url_for, session, request
from datetime import datetime
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.fields.html5 import DateField
languages = [
    ('aa', 'Afar'),
    ('ab', 'Abkhazian'),
    ('af', 'Afrikaans'),
    ('ak', 'Akan'),
    ('sq', 'Albanian'),
    ('am', 'Amharic'),
    ('ar', 'Arabic'),
    ('an', 'Aragonese'),
    ('hy', 'Armenian'),
    ('as', 'Assamese'),
    ('av', 'Avaric'),
    ('ae', 'Avestan'),
    ('ay', 'Aymara'),
    ('az', 'Azerbaijani'),
    ('ba', 'Bashkir'),
    ('bm', 'Bambara'),
    ('eu', 'Basque'),
    ('be', 'Belarusian'),
    ('bn', 'Bengali'),
    ('bh', 'Bihari languages'),
    ('bi', 'Bislama'),
    ('bo', 'Tibetan'),
    ('bs', 'Bosnian'),
    ('br', 'Breton'),
    ('bg', 'Bulgarian'),
    ('my', 'Burmese'),
    ('ca', 'Catalan; Valencian'),
    ('cs', 'Czech'),
    ('ch', 'Chamorro'),
    ('ce', 'Chechen'),
    ('zh', 'Chinese'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'),
    ('cv', 'Chuvash'),
    ('kw', 'Cornish'),
    ('co', 'Corsican'),
    ('cr', 'Cree'),
    ('cy', 'Welsh'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('dv', 'Divehi; Dhivehi; Maldivian'),
    ('nl', 'Dutch; Flemish'),
    ('dz', 'Dzongkha'),
    ('el', 'Greek, Modern (1453-)'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('eu', 'Basque'),
    ('ee', 'Ewe'),
    ('fo', 'Faroese'),
    ('fa', 'Persian'),
    ('fj', 'Fijian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('fy', 'Western Frisian'),
    ('ff', 'Fulah'),
    ('Ga', 'Georgian'),
    ('de', 'German'),
    ('gd', 'Gaelic; Scottish Gaelic'),
    ('ga', 'Irish'),
    ('gl', 'Galician'),
    ('gv', 'Manx'),
    ('el', 'Greek, Modern (1453-)'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian; Haitian Creole'),
    ('ha', 'Hausa'),
    ('he', 'Hebrew'),
    ('hz', 'Herero'),
    ('hi', 'Hindi'),
    ('ho', 'Hiri Motu'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('hy', 'Armenian'),
    ('ig', 'Igbo'),
    ('is', 'Icelandic'),
    ('io', 'Ido'),
    ('ii', 'Sichuan Yi; Nuosu'),
    ('iu', 'Inuktitut'),
    ('ie', 'Interlingue; Occidental'),
    ('ia', 'Interlingua (International Auxiliary Language Association)'),
    ('id', 'Indonesian'),
    ('ik', 'Inupiaq'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('jv', 'Javanese'),
    ('ja', 'Japanese'),
    ('kl', 'Kalaallisut; Greenlandic'),
    ('kn', 'Kannada'),
    ('ks', 'Kashmiri'),
    ('ka', 'Georgian'),
    ('kr', 'Kanuri'),
    ('kk', 'Kazakh'),
    ('km', 'Central Khmer'),
    ('ki', 'Kikuyu; Gikuyu'),
    ('rw', 'Kinyarwanda'),
    ('ky', 'Kirghiz; Kyrgyz'),
    ('kv', 'Komi'),
    ('kg', 'Kongo'),
    ('ko', 'Korean'),
    ('kj', 'Kuanyama; Kwanyama'),
    ('ku', 'Kurdish'),
    ('lo', 'Lao'),
    ('la', 'Latin'),
    ('lv', 'Latvian'),
    ('li', 'Limburgan; Limburger; Limburgish'),
    ('ln', 'Lingala'),
    ('lt', 'Lithuanian'),
    ('lb', 'Luxembourgish; Letzeburgesch'),
    ('lu', 'Luba-Katanga'),
    ('lg', 'Ganda'),
    ('mk', 'Macedonian'),
    ('mh', 'Marshallese'),
    ('ml', 'Malayalam'),
    ('mi', 'Maori'),
    ('mr', 'Marathi'),
    ('ms', 'Malay'),
    ('Mi', 'Micmac'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('mt', 'Maltese'),
    ('mn', 'Mongolian'),
    ('mi', 'Maori'),
    ('ms', 'Malay'),
    ('my', 'Burmese'),
    ('na', 'Nauru'),
    ('nv', 'Navajo; Navaho'),
    ('nr', 'Ndebele, South; South Ndebele'),
    ('nd', 'Ndebele, North; North Ndebele'),
    ('ng', 'Ndonga'),
    ('ne', 'Nepali'),
    ('nl', 'Dutch; Flemish'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
    ('nb', 'Bokmål, Norwegian; Norwegian Bokmål'),
    ('no', 'Norwegian'),
    ('oc', 'Occitan (post 1500)'),
    ('oj', 'Ojibwa'),
    ('or', 'Oriya'),
    ('om', 'Oromo'),
    ('os', 'Ossetian; Ossetic'),
    ('pa', 'Panjabi; Punjabi'),
    ('fa', 'Persian'),
    ('pi', 'Pali'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ps', 'Pushto; Pashto'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('rn', 'Rundi'),
    ('ru', 'Russian'),
    ('sg', 'Sango'),
    ('sa', 'Sanskrit'),
    ('si', 'Sinhala; Sinhalese'),
    ('sk', 'Slovak'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('se', 'Northern Sami'),
    ('sm', 'Samoan'),
    ('sn', 'Shona'),
    ('sd', 'Sindhi'),
    ('so', 'Somali'),
    ('st', 'Sotho, Southern'),
    ('es', 'Spanish; Castilian'),
    ('sq', 'Albanian'),
    ('sc', 'Sardinian'),
    ('sr', 'Serbian'),
    ('ss', 'Swati'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('ty', 'Tahitian'),
    ('ta', 'Tamil'),
    ('tt', 'Tatar'),
    ('te', 'Telugu'),
    ('tg', 'Tajik'),
    ('tl', 'Tagalog'),
    ('th', 'Thai'),
    ('bo', 'Tibetan'),
    ('ti', 'Tigrinya'),
    ('to', 'Tonga (Tonga Islands)'),
    ('tn', 'Tswana'),
    ('ts', 'Tsonga'),
    ('tk', 'Turkmen'),
    ('tr', 'Turkish'),
    ('tw', 'Twi'),
    ('ug', 'Uighur; Uyghur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('ve', 'Venda'),
    ('vi', 'Vietnamese'),
    ('vo', 'Volapük'),
    ('cy', 'Welsh'),
    ('wa', 'Walloon'),
    ('wo', 'Wolof'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('za', 'Zhuang; Chuang'),
    ('zh', 'Chinese'),
    ('zu', 'Zulu')
]
countries = [
    ('AF', u'Afghanistan'),
    ('AX', u'\xc5land Islands'),
    ('AL', u'Albania'),
    ('DZ', u'Algeria'),
    ('AS', u'American Samoa'),
    ('AD', u'Andorra'),
    ('AO', u'Angola'),
    ('AI', u'Anguilla'),
    ('AQ', u'Antarctica'),
    ('AG', u'Antigua and Barbuda'),
    ('AR', u'Argentina'),
    ('AM', u'Armenia'),
    ('AW', u'Aruba'),
    ('AU', u'Australia'),
    ('AT', u'Austria'),
    ('AZ', u'Azerbaijan'),
    ('BS', u'Bahamas'),
    ('BH', u'Bahrain'),
    ('BD', u'Bangladesh'),
    ('BB', u'Barbados'),
    ('BY', u'Belarus'),
    ('BE', u'Belgium'),
    ('BZ', u'Belize'),
    ('BJ', u'Benin'),
    ('BM', u'Bermuda'),
    ('BT', u'Bhutan'),
    ('BO', u'Bolivia, Plurinational State of'),
    ('BQ', u'Bonaire, Sint Eustatius and Saba'),
    ('BA', u'Bosnia and Herzegovina'),
    ('BW', u'Botswana'),
    ('BV', u'Bouvet Island'),
    ('BR', u'Brazil'),
    ('IO', u'British Indian Ocean Territory'),
    ('BN', u'Brunei Darussalam'),
    ('BG', u'Bulgaria'),
    ('BF', u'Burkina Faso'),
    ('BI', u'Burundi'),
    ('KH', u'Cambodia'),
    ('CM', u'Cameroon'),
    ('CA', u'Canada'),
    ('CV', u'Cape Verde'),
    ('KY', u'Cayman Islands'),
    ('CF', u'Central African Republic'),
    ('TD', u'Chad'),
    ('CL', u'Chile'),
    ('CN', u'China'),
    ('CX', u'Christmas Island'),
    ('CC', u'Cocos (Keeling Islands)'),
    ('CO', u'Colombia'),
    ('KM', u'Comoros'),
    ('CG', u'Congo'),
    ('CD', u'Congo, The Democratic Republic of the'),
    ('CK', u'Cook Islands'),
    ('CR', u'Costa Rica'),
    ('CI', u"C\xf4te D'ivoire"),
    ('HR', u'Croatia'),
    ('CU', u'Cuba'),
    ('CW', u'Cura\xe7ao'),
    ('CY', u'Cyprus'),
    ('CZ', u'Czech Republic'),
    ('DK', u'Denmark'),
    ('DJ', u'Djibouti'),
    ('DM', u'Dominica'),
    ('DO', u'Dominican Republic'),
    ('EC', u'Ecuador'),
    ('EG', u'Egypt'),
    ('SV', u'El Salvador'),
    ('GQ', u'Equatorial Guinea'),
    ('ER', u'Eritrea'),
    ('EE', u'Estonia'),
    ('ET', u'Ethiopia'),
    ('FK', u'Falkland Islands (Malvinas)'),
    ('FO', u'Faroe Islands'),
    ('FJ', u'Fiji'),
    ('FI', u'Finland'),
    ('FR', u'France'),
    ('GF', u'French Guiana'),
    ('PF', u'French Polynesia'),
    ('TF', u'French Southern Territories'),
    ('GA', u'Gabon'),
    ('GM', u'Gambia'),
    ('GE', u'Georgia'),
    ('DE', u'Germany'),
    ('GH', u'Ghana'),
    ('GI', u'Gibraltar'),
    ('GR', u'Greece'),
    ('GL', u'Greenland'),
    ('GD', u'Grenada'),
    ('GP', u'Guadeloupe'),
    ('GU', u'Guam'),
    ('GT', u'Guatemala'),
    ('GG', u'Guernsey'),
    ('GN', u'Guinea'),
    ('GW', u'Guinea-bissau'),
    ('GY', u'Guyana'),
    ('HT', u'Haiti'),
    ('HM', u'Heard Island and McDonald Islands'),
    ('VA', u'Holy See (Vatican City State)'),
    ('HN', u'Honduras'),
    ('HK', u'Hong Kong'),
    ('HU', u'Hungary'),
    ('IS', u'Iceland'),
    ('IN', u'India'),
    ('ID', u'Indonesia'),
    ('IR', u'Iran, Islamic Republic of'),
    ('IQ', u'Iraq'),
    ('IE', u'Ireland'),
    ('IM', u'Isle of Man'),
    ('IL', u'Israel'),
    ('IT', u'Italy'),
    ('JM', u'Jamaica'),
    ('JP', u'Japan'),
    ('JE', u'Jersey'),
    ('JO', u'Jordan'),
    ('KZ', u'Kazakhstan'),
    ('KE', u'Kenya'),
    ('KI', u'Kiribati'),
    ('KP', u"Korea, Democratic People's Republic of"),
    ('KR', u'Korea, Republic of'),
    ('KW', u'Kuwait'),
    ('KG', u'Kyrgyzstan'),
    ('LA', u"Lao People's Democratic Republic"),
    ('LV', u'Latvia'),
    ('LB', u'Lebanon'),
    ('LS', u'Lesotho'),
    ('LR', u'Liberia'),
    ('LY', u'Libya'),
    ('LI', u'Liechtenstein'),
    ('LT', u'Lithuania'),
    ('LU', u'Luxembourg'),
    ('MO', u'Macao'),
    ('MK', u'Macedonia, The Former Yugoslav Republic of'),
    ('MG', u'Madagascar'),
    ('MW', u'Malawi'),
    ('MY', u'Malaysia'),
    ('MV', u'Maldives'),
    ('ML', u'Mali'),
    ('MT', u'Malta'),
    ('MH', u'Marshall Islands'),
    ('MQ', u'Martinique'),
    ('MR', u'Mauritania'),
    ('MU', u'Mauritius'),
    ('YT', u'Mayotte'),
    ('MX', u'Mexico'),
    ('FM', u'Micronesia, Federated States of'),
    ('MD', u'Moldova, Republic of'),
    ('MC', u'Monaco'),
    ('MN', u'Mongolia'),
    ('ME', u'Montenegro'),
    ('MS', u'Montserrat'),
    ('MA', u'Morocco'),
    ('MZ', u'Mozambique'),
    ('MM', u'Myanmar'),
    ('NA', u'Namibia'),
    ('NR', u'Nauru'),
    ('NP', u'Nepal'),
    ('NL', u'Netherlands'),
    ('NC', u'New Caledonia'),
    ('NZ', u'New Zealand'),
    ('NI', u'Nicaragua'),
    ('NE', u'Niger'),
    ('NG', u'Nigeria'),
    ('NU', u'Niue'),
    ('NF', u'Norfolk Island'),
    ('MP', u'Northern Mariana Islands'),
    ('NO', u'Norway'),
    ('OM', u'Oman'),
    ('PK', u'Pakistan'),
    ('PW', u'Palau'),
    ('PS', u'Palestinian Territory, Occupied'),
    ('PA', u'Panama'),
    ('PG', u'Papua New Guinea'),
    ('PY', u'Paraguay'),
    ('PE', u'Peru'),
    ('PH', u'Philippines'),
    ('PN', u'Pitcairn'),
    ('PL', u'Poland'),
    ('PT', u'Portugal'),
    ('PR', u'Puerto Rico'),
    ('QA', u'Qatar'),
    ('RE', u'R\xe9union'),
    ('RO', u'Romania'),
    ('RU', u'Russian Federation'),
    ('RW', u'Rwanda'),
    ('BL', u'Saint Barth\xe9lemy'),
    ('SH', u'Saint Helena, Ascension and Tristan Da Cunha'),
    ('KN', u'Saint Kitts and Nevis'),
    ('LC', u'Saint Lucia'),
    ('MF', u'Saint Martin (French Part)'),
    ('PM', u'Saint Pierre and Miquelon'),
    ('VC', u'Saint Vincent and the Grenadines'),
    ('WS', u'Samoa'),
    ('SM', u'San Marino'),
    ('ST', u'Sao Tome and Principe'),
    ('SA', u'Saudi Arabia'),
    ('SN', u'Senegal'),
    ('RS', u'Serbia'),
    ('SC', u'Seychelles'),
    ('SL', u'Sierra Leone'),
    ('SG', u'Singapore'),
    ('SX', u'Sint Maarten (Dutch Part)'),
    ('SK', u'Slovakia'),
    ('SI', u'Slovenia'),
    ('SB', u'Solomon Islands'),
    ('SO', u'Somalia'),
    ('ZA', u'South Africa'),
    ('GS', u'South Georgia and the South Sandwich Islands'),
    ('SS', u'South Sudan'),
    ('ES', u'Spain'),
    ('LK', u'Sri Lanka'),
    ('SD', u'Sudan'),
    ('SR', u'Suriname'),
    ('SJ', u'Svalbard and Jan Mayen'),
    ('SZ', u'Swaziland'),
    ('SE', u'Sweden'),
    ('CH', u'Switzerland'),
    ('SY', u'Syrian Arab Republic'),
    ('TW', u'Taiwan, Province of China'),
    ('TJ', u'Tajikistan'),
    ('TZ', u'Tanzania, United Republic of'),
    ('TH', u'Thailand'),
    ('TL', u'Timor-leste'),
    ('TG', u'Togo'),
    ('TK', u'Tokelau'),
    ('TO', u'Tonga'),
    ('TT', u'Trinidad and Tobago'),
    ('TN', u'Tunisia'),
    ('TR', u'Turkey'),
    ('TM', u'Turkmenistan'),
    ('TC', u'Turks and Caicos Islands'),
    ('TV', u'Tuvalu'),
    ('UG', u'Uganda'),
    ('UA', u'Ukraine'),
    ('AE', u'United Arab Emirates'),
    ('GB', u'United Kingdom'),
    ('US', u'United States'),
    ('UM', u'United States Minor Outlying Islands'),
    ('UY', u'Uruguay'),
    ('UZ', u'Uzbekistan'),
    ('VU', u'Vanuatu'),
    ('VE', u'Venezuela, Bolivarian Republic of'),
    ('VN', u'Viet Nam'),
    ('VG', u'Virgin Islands, British'),
    ('VI', u'Virgin Islands, U.S.'),
    ('WF', u'Wallis and Futuna'),
    ('EH', u'Western Sahara'),
    ('YE', u'Yemen'),
    ('ZM', u'Zambia'),
    ('ZW', u'Zimbabwe')
]
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
            flash('Bu sayfayı görüntülemek için lütfen giriş yapın', 'danger')
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
    return render_template('birthdaylist.html', birthdays=birthdays)


class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country[0], country[1]) for country in countries]


class LanguageSelectField(SelectField):
    def __init__(self, *args, **kwargs):

        super(LanguageSelectField, self).__init__(*args, **kwargs)
        self.choices = [(language[0], language[1]) for language in languages]


# dashboard
@app.route('/dashboard', methods=['POST', "GET"])
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
        name = StringField("İsim", default=name_value, validators=[
            validators.Length(min=4, max=25), validators.DataRequired(message="Lütfen bir isim belirleyin")])
        surname = StringField("Soy isim", default=surname_value, validators=[
            validators.Length(min=4, max=25), validators.DataRequired(message="Lütfen bir soyisim belirleyin")])
        email = StringField("E-mail", default=email_value, validators=[validators.Email(
            message="Lütfen Geçerli bir email adresi giriniz."), validators.DataRequired(message="Lütfen bir email belirleyin")])
        telno = StringField("Telefon numarası", default=telno_value, validators=[
            validators.Length(min=4, max=25), validators.DataRequired(message="Lütfen bir telefon no belirleyin")])
        username = StringField("Kullanıcı adı", default=username_value, validators=[
            validators.Length(min=5, max=15), validators.DataRequired(message="Lütfen bir kullanıcı adı belirleyin")])
        try:
            birthday = DateField("Doğum gününüz", format='%Y-%m-%d',
                                 default=datetime.strptime(birthday_value, '%Y-%m-%d'))
        except TypeError:
            birthday = DateField("Doğum gününüz")
        education = StringField("Eğitim Bilgileri", default=education_value, validators=[
            validators.Length(min=4, max=25), validators.DataRequired(message="Lütfen eğitim durumunuzu belirleyin")])
        section = StringField("Bölümünüz", default=section_value, validators=[
            validators.Length(min=4, max=25), validators.DataRequired(message="Lütfen bölümünüzü belirleyin")])
        country = CountrySelectField("Ülkeniz", default=country_value)
        language = LanguageSelectField("Diliniz", default=language_value)

    form = DashboardForm(request.form)

    if request.method == "POST" and form.validate():
        user = User.query.filter_by(id=account_id).first()

        if form.email.data != user.email:
            if User.query.filter_by(email=form.email.data).first():
                flash("Email kullanılıyor.", "danger")
                return render_template('dashboard.html', form=form)
            else:
                user.email = form.email.data
        if form.telno.data != str(user.telno):
            if User.query.filter_by(telno=form.telno.data).first():
                flash("Telefon Numarası kullanılıyor.", "danger")
                return render_template('dashboard.html', form=form)
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
        flash("Profil Başarıyla Kaydedildi.", "success")

    session_refresh(form.username.data)
    return render_template('dashboard.html', form=form)

# silme


@app.route('/delete/<string:id>')
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('logout'))

# bloglarım


@app.route('/myblogs')
@login_required
def myblogs():
    posts = Post.query.all()
    posts.reverse()
    for i in posts:
        if i.username == session['username']:
            pass
        else:
            posts.remove(i)
    return render_template('myblogs.html', posts=posts)

# bloglarımı sil


@app.route('/dellpost/<string:id>')
@login_required
def dellpost(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('myblogs'))


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

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(80))
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    time = db.Column(db.String(80))
    section = db.Column(db.String(80))
    username = db.Column(db.String(80))

    def __repr__(self):
        return '<Post %r>' % self.id


class RegisterForm(Form):
    username = StringField("Kullanıcı Adı", validators=[
                           validators.Length(min=5, max=11), validators.DataRequired(message="Lütfen bir kullanıcı adı belirleyin")])
    email = StringField("Email Adresi", validators=[validators.Email(
        message="Lütfen Geçerli bir email adresi giriniz."), validators.DataRequired(message="Lütfen bir email belirleyin")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname="confirm",
                           message="Parolanız uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")


class LoginForm(Form):
    username = StringField("Kullanıcı Adı", validators=[
                           validators.Length(min=5, max=35), validators.DataRequired(message="Lütfen bir kullanıcı adı belirleyin")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyin"),
    ])


class AddPostForm(Form):
    area = TextAreaField('Text', render_kw={"rows": 10, "cols": 11})


# session yenileme"
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

# kayıt


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        newUser = User(username=username, email=email, password=password)
        if User.query.filter_by(username=username).first():
            flash("Kullanıcı adı kullanılıyor..", "danger")
            return render_template('register.html', form=form)
            print("sorun var kullanıcı adı")
        else:
            if User.query.filter_by(email=email).first():
                flash("Email kullanılıyor..", "danger")
                return render_template('register.html', form=form)
                print("sorun var email")
            else:
                db.session.add(newUser)
                db.session.commit()
                session_refresh(username)
                print("kayıt oldu")
                flash("Başarıyla kayıt oldunuz.", "success")
                return redirect(url_for('dashboard'))

    else:
        print("büyük sorun")
        return render_template('register.html', form=form)

# giriş


@app.route('/login', methods=["POST", "GET"])
def login():

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        usernameEntered = form.username.data
        passwordEntered = (form.password.data)
        usernameFromDB = User.query.filter_by(
            username=usernameEntered).first().username
        passwordFromDB = User.query.filter_by(
            username=usernameEntered).first().password

        if usernameFromDB == usernameEntered:
            if sha256_crypt.verify(passwordEntered, passwordFromDB):
                flash("Başarıyla giriş yaptınız.", "success")
                session_refresh(usernameEntered)
                return redirect(url_for('dashboard'))
            else:
                flash("Parolanızı yanlış girdiniz.", "danger")
                return render_template("login.html", form=form)
        else:
            flash("Böyle bir kullanıcı bulunmuyor.", "danger")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/addpost", methods=["GET", "POST"])
@login_required
def addpost():
    AddPostForm.area = TextAreaField('Text', render_kw={"rows": 10, "cols": 11})
    form = AddPostForm(request.form)
    if request.method == "POST" and form.validate():
        if session['name']:
            if session['surname']:
                if session['section']:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    post = form.area.data
                    newPost = Post(post=post, name=session['name'], surname=session['surname'],
                                   time=dt_string, section=session['section'], username=session['username'])
                    db.session.add(newPost)
                    db.session.commit()
                    flash("Post başarıyla paylaşıldı.", "success")
                    return redirect(url_for('blogs'))
                else:
                    flash(
                        "Post paylaşılamadı. Profil bölümünden bölümünüzü belirleyiniz.", "danger")
            else:
                flash(
                    "Post paylaşılamadı. Profil bölümünden soyisminizi belirleyiniz.", "danger")
        else:
            flash(
                "Post paylaşılamadı. Profil bölümünden isminizi belirleyiniz.", "danger")

    return render_template("addpost.html", form=form)


@app.route("/editpost/<string:id>", methods=["GET", "POST"])
@login_required
def editpost(id):
    blog = Post.query.filter_by(id=id).first()
    
    AddPostForm.area = TextAreaField('Text', render_kw={"rows": 10, "cols": 11},default=blog.post)
    form = AddPostForm(request.form)

    if request.method == "POST" and form.validate():

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        blog.post = form.area.data
        blog.time = dt_string
        print(blog.post,form.area.data)
        db.session.commit()
        flash("Post başarıyla düzenlendi.", "success")
        return redirect(url_for('myblogs'))

    return render_template("editpost.html", form=form)


@app.route("/blogs")
def blogs():
    posts = Post.query.all()
    posts.reverse()

    return render_template("blogs.html", posts=posts)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Çıkış yapıldı", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
