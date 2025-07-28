from flask import flash, jsonify, redirect, render_template, request, session, url_for

from app.models import User
from app.config import db


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
        if request.method == 'POST':
            data = request.get_json()

            if not data:
                return jsonify({"message": "Invalid request, expected JSON"}), 400
                
            existing_user = User.query.filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"message": "Email already registered"}), 400
            
            new_user = User(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                phone=data["phone"],
                address=data["address"],
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                return jsonify({"message": "Registration successful"}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Error registering user", "error": str(e)}), 500
        
        return render_template('register.html')