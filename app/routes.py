from flask import flash, redirect, render_template, request, session, url_for

from app.models import User


def init_routes(app):
    
    @app.route('/')
    def initial():
        return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']        
            user = User.query.filter_by(email=email, password=password).first()

            if user:
                session['user_id'] = user.user_id
                return redirect(url_for('home'))
            else:
                flash("Invalid email or password", "danger")

        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        pass