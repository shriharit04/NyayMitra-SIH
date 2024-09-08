from flask import Flask, jsonify, request
from flask_cors import CORS
from Chatbot.chatbotRoutes import chatbot_bp  # Import the Blueprint

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for /api routes

# Register the Blueprint with a URL prefix
app.register_blueprint(chatbot_bp,url_prefix='/api/chatbot')

@app.route('/', methods=['GET'])
def get_data():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({'received': data}), 201

if __name__ == '__main__':
    app.run(port=5000)  # Default port is 5000
