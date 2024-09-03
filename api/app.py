from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for /api routes

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)

@app.route('/api/chatbot/prompt', methods=['GET'])
def prompt():
    user_prompt = request.args.get('prompt')
    result = {"data": f"prompt entered {user_prompt}"}
    return jsonify(result)

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({'received': data}), 201

if __name__ == '__main__':
    app.run(port=5000)  # Default port is 5000
