from flask import flash, jsonify, redirect, render_template, request, session, url_for

from app.models import Tool, User
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
    

    @app.route('/home')
    def home():
        return render_template('home.html')
    
    @app.route('/get_tools', methods=['GET'])
    def get_tools():
        current_user_id = session.get('user_id')
        tools = Tool.query.filter((Tool.user_id != current_user_id) & (Tool.status == 'Available')).all()
        tools_data =[tool.to_dict() for tool in tools]
        return jsonify(tools_data)
    

    @app.route('/mytools')
    def my_tools():
        return render_template('my_tools.html')
    
    
    @app.route('/get_my_tools', methods=['GET'])
    def get_my_tools():
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'User not logged in'}), 401

        tools = Tool.query.filter_by(user_id=current_user_id).all()
        tool_list = [tool.to_dict() for tool in tools]

        return jsonify({'tools': tool_list})