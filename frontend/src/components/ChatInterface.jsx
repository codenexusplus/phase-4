import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import API_BASE_URL from '../api';

const ChatInterface = ({ onTaskUpdate }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);
  const { token, user } = useAuth();

  // WebSocket connection state
  const wsRef = useRef(null);
  const [wsConnected, setWsConnected] = useState(false);

  // Initialize WebSocket connection
  useEffect(() => {
    // Attempt to establish WebSocket connection for real-time updates
    const connectWebSocket = () => {
      try {
        // Check if API_BASE_URL is valid before creating WebSocket connection
        if (!API_BASE_URL) {
          console.error('API_BASE_URL is not defined. Cannot establish WebSocket connection.');
          return;
        }

        // Convert API_BASE_URL from http(s) to ws(s)
        let wsUrl;
        if (API_BASE_URL.includes('localhost:8000')) {
          // Special case for local development: use port 3001 for WebSocket
          wsUrl = 'ws://localhost:3001/ws';
        } else {
          // For other environments, derive WebSocket URL from API_BASE_URL
          wsUrl = API_BASE_URL.replace(/^http/, 'ws') + '/ws';
        }

        console.log('Attempting to connect to WebSocket:', wsUrl);

        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
          console.log('WebSocket connected');
          setWsConnected(true);
          wsRef.current = ws;
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            // Handle incoming WebSocket messages
            if (data.type === 'task_update') {
              // Trigger task update if the AI performed an action that affects tasks
              if (onTaskUpdate) {
                onTaskUpdate();
              }
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setWsConnected(false);
        };

        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setWsConnected(false);
          wsRef.current = null;

          // Attempt to reconnect after a delay (but only if user is still authenticated)
          if (user && token) {
            setTimeout(connectWebSocket, 5000);
          }
        };

        // Store WebSocket reference
        wsRef.current = ws;
      } catch (error) {
        console.error('Error initializing WebSocket:', error);
        setWsConnected(false);
      }
    };

    // Only attempt WebSocket connection if user is authenticated
    if (user && token) {
      connectWebSocket();
    }

    // Cleanup function
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [user, token, onTaskUpdate]);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle sending a message
  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim() || !user || !token) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send the message to the backend with authentication
      const response = await axios.post(`${API_BASE_URL}/api/${user.id}/chat`, {
        message: inputValue,
        conversation_id: conversationId
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      // Update conversation ID if it was created
      if (response.data.conversation_id && !conversationId) {
        setConversationId(response.data.conversation_id);
      }

      // Add AI response to the chat
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.data.response || response.data.error || 'Sorry, I encountered an error.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);

      // Trigger task update if the AI performed an action that affects tasks
      if (response.data.action_performed && onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!user || !token) {
    return (
      <div className="chat-container">
        <div className="chat-messages">
          <div className="welcome-message">
            <h3>Please log in to use the AI Todo Assistant</h3>
            <p>The chat functionality requires authentication.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>Hello! I'm your AI Todo Assistant</h3>
            <p>You can ask me to:</p>
            <ul>
              <li>Add tasks (e.g., "Add buy groceries to my list")</li>
              <li>View tasks (e.g., "Show me my pending tasks")</li>
              <li>Complete tasks (e.g., "Mark task #1 as complete")</li>
              <li>Delete tasks (e.g., "Delete task #2")</li>
              <li>Update tasks (e.g., "Change task #1 to 'buy organic groceries'")</li>
            </ul>
            <p>How can I help you today?</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <div className="message-content">
                {message.content}
              </div>
              <div className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">
              <em>Thinking...</em>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          disabled={isLoading}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="send-button"
        >
          Send
        </button>
      </form>

      {/* Show WebSocket connection status */}
      {wsConnected && (
        <div className="websocket-status connected">
          Connected to real-time updates
        </div>
      )}
      {!wsConnected && (
        <div className="websocket-status disconnected">
          Real-time updates not available
        </div>
      )}
    </div>
  );
};

export default ChatInterface;