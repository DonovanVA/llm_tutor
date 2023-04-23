import React from 'react';
import logo from './logo.svg';
import './App.css';
import cors from 'cors';

function App() {
  const [messages, setMessages] = React.useState<string[]>([]); // Initialize state with an empty array

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    
    const formData = new FormData(event.currentTarget);
    const requestData = {
      question: formData.get('question')
    };
    fetch('http://127.0.0.1:5000/ask', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
  })
  .then(response => response.json())
  .then(data => {
      setMessages([...messages, data.answer]);
  })
  .catch(error => {
      console.error('Error:', error)
  })
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="text" name="question" placeholder="Ask a question" />
        <button type="submit">Submit</button>
      </form>
      {messages.map((message: string, index: number) => {
        return (
          <div style={{ height: "200px", backgroundColor: index % 2 === 0 ? "#FFFFFF" : "#D9D9D9" }}>
            <p>{message}</p>
          </div>
        )
      })}
    </div>
  );
}

export default App;
