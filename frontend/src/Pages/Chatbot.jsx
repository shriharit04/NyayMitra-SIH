import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

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
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg max-w-4xl mx-auto mt-8 flex flex-col h-screen w-7/10">
      <div className="flex flex-col flex-grow overflow-y-auto mb-4">
        {chat.length === 0 && (
          <div className="text-center text-gray-400 mt-4">Type to chat...</div>
        )}
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
          className="border border-gray-400 rounded-lg p-2 resize-none overflow-hidden flex-grow mr-2 bg-gray-700 text-white"
        />
        <button
          type="submit"
          className="bg-gray-600 text-white rounded-lg p-2 hover:bg-gray-700 transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
          </svg>

        </button>
      </form>
    </div>
  );
}

export default Chatbot;
