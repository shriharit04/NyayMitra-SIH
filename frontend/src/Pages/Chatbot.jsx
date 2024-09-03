import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios'
function Chatbot() {
  const [chat, setChat] = useState([]);
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    // Adjust the textarea height based on content
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleNewPrompt = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      const userMessage = input;
      setInput('');
      try {
        const response = await axios.get('/api/chatbot/prompt', {
          params: { prompt: input }
        });
        const botResponse = response.data.data;
  
        // Update chat state with user message and bot response
        setChat([...chat, { user: userMessage }, { bot: botResponse }]);
      } catch (error) {
        console.error('Error:', error);
        // Optionally, you can add error handling logic or display an error message
        setChat([...chat, { user: userMessage }, { bot: 'Sorry, something went wrong.' }]);
      }
    }
  };
  

  return (
    <div className="bg-black p-4 rounded-lg shadow-lg max-w-4xl mx-auto mt-8 flex flex-col h-screen">
      <div className="flex flex-col flex-grow overflow-y-auto mb-4">
        {chat.map((message, index) => (
          <div key={index} className={`mb-2 ${message.user ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block px-4 py-2 rounded-lg ${message.user ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-800'}`}>
              {message.user || message.bot}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleNewPrompt} className="flex items-end">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={1}
          placeholder="Ask a question..."
          className="border border-gray-400 rounded-lg p-2 resize-none overflow-hidden flex-grow mr-2"
        />
        <button
          type="submit"
          className="bg-gray-500 text-white rounded-lg px-4 py-2 hover:bg-gray-600 transition"
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default Chatbot;
