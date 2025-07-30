from app.config import db

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.String(255), nullable=False)


class Tool(db.Model):
    __tablename__ = 'tools'
    
    tool_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', name='fk_user_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.String(10), nullable = False)
    status = db.Column(db.Enum('Available', 'Exchanged', name='tool_status'), default='Available')
    image = db.Column(db.String(100), nullable=False, unique=True)
    owner = db.relationship('User', backref=db.backref('owner', lazy=True))
    
    def to_dict(self):
        return{
            'tool_id': self.tool_id,
            'username': self.owner.name,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'status': self.status,
            'image': self.image,
            'address': self.owner.address,
        }
    

class BorrowRequest(db.Model):
    __tablename__ = 'borrow_requests'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.tool_id'), nullable=False)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Declined', 'Returned', name='request_status'), default='Pending')
    
    sender = db.relationship('User', foreign_keys=[requester_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    tool = db.relationship('Tool', foreign_keys=[tool_id])
    
    def to_dict(self):
        return{
            'req_id': self.request_id,
            'requesterName': self.sender.name,
            'receiverName': self.receiver.name,
            'name': self.tool.name,
            'description': self.tool.description,
            'toolStatus': self.tool.status,
            'reqStatus': self.status,
            'image': self.tool.image,
        }