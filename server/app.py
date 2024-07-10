from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_serializer = None  # Resetting to default JSON serialization behavior

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    message = db.session.query(Message).filter_by(id=id).first_or_404()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.query(Message).filter_by(id=id).first_or_404()
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
    if 'username' in data:
        message.username = data['username']
    message.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.query(Message).filter_by(id=id).first_or_404()
    db.session.delete(message)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555)
