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
        const response = await axios.post('/api/chatbot/test_prompt', {
          prompt: input
        });
        const botResponse = response.data.response;

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
    <div className='w-full h-full bg-gray-900 m-0 p-0'>
      <div className="bg-gray-950 p-4 rounded-lg shadow-lg max-w-4xl mx-auto flex flex-col h-screen w-3/5">

        <div className="flex flex-col flex-grow overflow-y-auto mb-4">
          {/* Placeholder for empty chat */}
          {chat.length === 0 ? (
            <div className="flex justify-center items-center h-full">
              <div className="text-gray-500 text-center">
                <h2 className="text-xl mb-4">Welcome to NyayMitra</h2>
                <p>Start a conversation to get legal assistance.</p>
              </div>
            </div>
          ) : (
            chat.map((message, index) => (
              <div key={index} className={`mb-2 ${message.user ? 'text-right' : 'text-left'}`}>
                <div className={`inline-block px-4 py-2 rounded-lg ${message.user ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-800'}`}>
                  {message.user || message.bot}
                </div>
              </div>
            ))
          )}
        </div>

        <form onSubmit={handleNewPrompt} className="flex items-end">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={1}
            placeholder="Ask your legal question..."
            className="bg-gray-900 text-white border border-gray-900 rounded-full p-2 resize-none overflow-hidden flex-grow mr-2"
          />
          <button type='submit'
          className='relative py-2 px-3 rounded-lg font-medium text-sm bg-gradient-to-b from-[#190D2E] to-[#4a208a] shadow-[0px_0px_12px_#8c45ff]'>
            <div className='absolute inset-0'>
              <div className="border rounded-lg border-white/20 absolute inset-0 [mask-image:linear-gradient(to_bottom,black,transparent)]"></div>
              <div className="border rounded-lg border-white/40 absolute inset-0 [mask-image:linear-gradient(to_top,black,transparent)]"></div>
              <div className="absolute inset-0 shadow[0_0_10px_rgb(140,69,255.7)] rounded-lg"></div>
            </div>
            <span>Enter</span>
          </button>
        </form>

        <div className='flex justify-center items-center'>
          <p className='text-gray-700 mt-1 text-sm'>
            NyayMitra only provides knowledge based on previous case data. It is not a substitute for a lawyer.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;
