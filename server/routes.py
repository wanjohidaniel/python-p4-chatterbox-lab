from flask import Blueprint, jsonify, request
from app import db
from models import Message

message_routes = Blueprint('message_routes', __name__)

@message_routes.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.__dict__ for message in messages])

@message_routes.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.__dict__)

@message_routes.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.json
    message.body = data.get('body', message.body)
    db.session.commit()
    return jsonify(message.__dict__)

@message_routes.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'})

