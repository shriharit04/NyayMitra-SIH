import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './Navbar';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatSessionId, setChatSessionId] = useState(null);

  // On initial load, start a new chat session
  useEffect(() => {
    const startNewChat = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/new_chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        setChatSessionId(data.chat_session_id);
      } catch (error) {
        console.error('Error starting new chat session:', error);
      }
    };

    startNewChat();
  }, []);

  const sendMessage = async () => {
    if (input.trim() === "" || !chatSessionId) return;

    const userMessage = { text: input, sender: "user" };

    // Add user message to the chat
    setMessages([...messages, userMessage]);

    // Send the message to Flask backend and handle streaming response
    try {
      const response = await fetch('http://localhost:5000/api/send_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_session_id: chatSessionId,
          message: input  
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let botMessage = { text: '', sender: 'bot' };

      // Initialize botMessage in the messages list
      setMessages((prevMessages) => [...prevMessages, botMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });

        // Append the chunk of bot response progressively
        botMessage.text += chunk;
        setMessages((prevMessages) =>
          prevMessages.map((msg, index) =>
            index === prevMessages.length - 1 ? { ...botMessage } : msg
          )
        );
      }

      // After the stream ends, ensure the final message is saved
      setMessages((prevMessages) =>
        prevMessages.map((msg, index) =>
          index === prevMessages.length - 1 ? { ...botMessage } : msg
        )
      );

    } catch (error) {
      console.error("Error sending message to backend", error);
    }

    setInput('');
  };

  return (
    <div className="App">
      <Navbar /> {/* Sidebar on the left */}
      
      <div className="chat"> {/* Main chat content */}
        <h2>DOJChat</h2>
        <div className="chat-window">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender}`}
              dangerouslySetInnerHTML={{ __html: msg.text }}
            />
          ))}
        </div>

        <div className="input-area">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
