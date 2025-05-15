from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from storage import add_user, add_visitor
from models import db, User, Visitor

app = Flask(__name__)
app.secret_key = 'secret_key_example'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///otel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Öncelikle giriş yapmalısınız.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', background_class='index-background')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Başarıyla giriş yapıldı.')
            return redirect(url_for('dashboard'))
        else:
            flash('Kullanıcı adı / e-posta veya şifre hatalı.')
            return redirect(url_for('login'))

    return render_template('login.html', background_class='login-background')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Çıkış yapıldı.')
    return redirect(url_for('login'))

@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Şifreler eşleşmiyor.')
            return redirect(url_for('create_account'))

        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            flash('Bu e-posta veya kullanıcı adı zaten kayıtlı.')
            return redirect(url_for('create_account'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        add_user({
            "username": username,
            "email": email,
            "created_at": datetime.utcnow().isoformat()
        })
        flash('Hesap başarıyla oluşturuldu. Giriş yapabilirsiniz.')
        return redirect(url_for('login'))

    return render_template('createaccount.html', background_class='createaccount-background')


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register_visitor():
    if request.method == 'POST':
        visitor = Visitor(
            name=request.form['name'],
            surname=request.form['surname'],
            phone=request.form['phone'],
            email=request.form.get('email'),
            room=request.form['room']
        )
        db.session.add(visitor)
        db.session.commit()
        add_visitor({
            "name": request.form['name'],
            "surname": request.form['surname'],
            "email": request.form.get('email'),
            "phone": request.form['phone'],
            "room": request.form['room'],
            "visit_date": datetime.utcnow().isoformat()
        })
        flash('Ziyaretçi kaydı başarıyla oluşturuldu.')
        return redirect(url_for('dashboard'))
    return render_template('register.html', background_class='register-background')


@app.route('/dashboard')
@login_required
def dashboard():
    visitors = Visitor.query.order_by(Visitor.visit_date.desc()).all()
    return render_template('dashboard.html', visitors=visitors, background_class='dashboard-background')

@app.route('/visitor/<int:visitor_id>')
@login_required
def visitor_detail(visitor_id):
    visitor = Visitor.query.get_or_404(visitor_id)
    return render_template('visitor_detail.html', visitor=visitor, background_class='visitor-detail-background')

@app.route('/edit/<int:visitor_id>', methods=['GET', 'POST'])
@login_required
def edit_visitor(visitor_id):
    visitor = Visitor.query.get_or_404(visitor_id)
    if request.method == 'POST':
        visitor.name = request.form['name']
        visitor.surname = request.form['surname']
        visitor.email = request.form['email']
        visitor.phone = request.form['phone']
        visitor.room = request.form['room']
        db.session.commit()
        flash('Ziyaretçi bilgileri güncellendi.')
        return redirect(url_for('dashboard'))
    return render_template('edit_visitor.html', visitor=visitor, background_class='editvisitor-background')

@app.route('/delete/<int:visitor_id>', methods=['POST', 'GET'])
@login_required
def delete_visitor(visitor_id):
    visitor = Visitor.query.get(visitor_id)
    if visitor is None:
        flash('Ziyaretçi bulunamadı.')
        return redirect(url_for('dashboard'))
    db.session.delete(visitor)
    db.session.commit()
    flash('Ziyaretçi silindi.')
    return redirect(url_for('dashboard'))

@app.route('/visitors')
@login_required
def visitors_list():
    visitors = Visitor.query.order_by(Visitor.visit_date.desc()).all()
    return render_template('visitors.html', visitors=visitors)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

