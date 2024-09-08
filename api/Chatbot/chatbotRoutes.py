from flask import Blueprint, jsonify, request
from .chatbot import loading, generate

# Define the Blueprint
chatbot_bp = Blueprint('chatbot_bp', __name__)

# Initialize the RAG chain
rag_chain = loading()
from langchain.memory import ChatMessageHistory
history = ChatMessageHistory()


@chatbot_bp.route('/')
def home():
    return "Welcome to the Chatbot Page!"


@chatbot_bp.route('/initial_load', methods=['GET'])
def initial_load():
    # Initialize the RAG chain (if not already initialized)
    global rag_chain
    rag_chain = loading()
    result = {"data": "Initialization complete"}
    return jsonify(result)



@chatbot_bp.route('/test_prompt', methods=['POST'])
def prompt():
    user_prompt = request.json.get('prompt')
    result = {"data": f"Prompt entered: {user_prompt}"}
    return jsonify(result)





@chatbot_bp.route('/prompt', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query', '')
    response = generate(rag_chain, query)
    return jsonify({"response": response}), 200
