from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from groq import Groq

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

client = Groq(api_key="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")

with app.app_context():
    db.create_all()

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    conversations = db.relationship('Conversation', backref='chat_session', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    bot_response = db.Column(db.String(500), nullable=False)
    chat_session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)

@app.route('/api/new_chat', methods=['POST'])
def new_chat():
    new_session = ChatSession()
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'chat_session_id': new_session.id})

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    chat_session_id = data.get('chat_session_id')
    user_message = data.get('message')

    if not chat_session_id or not user_message:
        return jsonify({'error': 'Invalid input'}), 400

    chat_session = db.session.get(ChatSession, chat_session_id)
    if not chat_session:
        return jsonify({'error': 'Chat session not found'}), 404

    # Retrieve conversation history for the session
    conversations = Conversation.query.filter_by(chat_session_id=chat_session_id).order_by(Conversation.id).all()
    messages = [{'role': 'user', 'content': convo.user_message} for convo in conversations]


    initial_context = "You work for the Department of Justice and are an educational bot named Arjun that provides replies based on evidence."
    messages.insert(0, {'role': 'system', 'content': initial_context})
    

    # Add the new user message
    messages.append({'role': 'user', 'content': user_message})

    def generate_response():
        with app.app_context():  
            try:
                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=messages,
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stream=True,
                    stop=None,  
                )

                bot_response = ""
                for chunk in completion:
                    part = chunk.choices[0].delta.content or ""
                    bot_response += part
                    yield part  # Stream the response part to the client

                conversation = Conversation(
                    user_message=user_message,
                    bot_response=bot_response,
                    chat_session_id=chat_session.id
                )
                db.session.add(conversation)
                db.session.commit()

            except Exception as e:
                print(f"Error from Groq API: {e}")
                yield 'Error: Failed to get a response from Groq API'

    return Response(generate_response(), content_type='text/plain')





if __name__ == '__main__':
    app.run(debug=True)
