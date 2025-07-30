import os
import uuid
from flask import current_app, flash, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from werkzeug.utils import secure_filename
from app.models import Tool, User, BorrowRequest
from app.config import db


def init_routes(app):

    @app.route('/uploads/images/<path:filename>')
    def image_file(filename):
        return send_from_directory('uploads/images', filename)
    
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
    
    @app.route('/view_tool/<int:tool_id>')
    def view_tool(tool_id):
        tool = Tool.query.get(tool_id)
        if not tool:
            return "Book not found", 404

        return render_template('tool_details.html', tool=tool)
    

    @app.route('/addtool', methods=['GET', 'POST'])
    def add_tool():
        if request.method == 'GET':
            return render_template('add_tools.html')

        if request.method == 'POST':
            current_user_id = session.get('user_id')
            if not current_user_id:
                return jsonify({'error': 'User not logged in'}), 401
            
            name = request.form.get('title')
            description = request.form.get('description', '')
            
            file = request.files['toolImage']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            
            print(unique_filename)
                    
            new_tool = Tool(
                user_id=current_user_id,
                name=name,
                description=description,
                status='Available',
                image=unique_filename
            )

            db.session.add(new_tool)
            db.session.commit()

        return jsonify({'success': True, 'message': 'Tool added successfully!'})
        

    @app.route('/borrow_tool/<int:tool_id>', methods=['POST'])
    def borrow_tool(tool_id):
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'User not logged in'}), 401

        tool = Tool.query.get(tool_id)
        if not tool:
            return jsonify({'error': 'Tool not found'}), 404

        if tool.user_id == current_user_id:
            return jsonify({'error': 'You cannot borrow your own tool'}), 400

        if tool.status == 'Exchanged':
            return jsonify({'error': 'Tool already exchanged'}), 400

        new_request = BorrowRequest(requester_id=current_user_id, receiver_id=tool.user_id, tool_id=tool_id)
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Tool requested successfully!'})
    

    @app.route('/delete_tool/<int:tool_id>', methods=['POST', 'GET'])
    def delete(tool_id):
        tool = Tool.query.get(tool_id)
        if tool:
            db.session.delete(tool)
            db.session.commit()
            return {'message': 'Tool deleted successfully'}, 200
        else:
            return {'message': 'Tool not found'}, 404
        

    @app.route('/history')
    def my_history():
        user_id = session.get('user_id')
    
        if not user_id:
            return redirect('/login')

        borrow_requests = BorrowRequest.query.filter_by(receiver_id=user_id, status='Pending').all()
        print("A",borrow_requests, user_id)
        
        tools_exchanged = (
        BorrowRequest.query
        .join(Tool, BorrowRequest.tool_id == Tool.tool_id)
        .filter(
            BorrowRequest.receiver_id==user_id, 
            Tool.status == 'Exchanged'
            )
        .all()
        )
        print("B",tools_exchanged)

        borrowed_requests = BorrowRequest.query.filter(
            BorrowRequest.requester_id == user_id
        ).all()
        borrowed_tools = [req for req in borrowed_requests]
        print("C",borrowed_tools)

        return render_template('history.html', borrow_requests=borrow_requests,  tools_exchanged=tools_exchanged, tools_borrowed=borrowed_tools)
    

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))