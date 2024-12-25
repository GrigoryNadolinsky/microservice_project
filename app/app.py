from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/microservice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id, 'name': new_item.name, 'description': new_item.description}), 201

@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    data = request.json
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})

@app.route('/')
def home():
    return "Welcome to the Microservice API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
