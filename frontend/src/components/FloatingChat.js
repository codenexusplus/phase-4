import React from 'react';
import ChatInterface from './ChatInterface'; // Import the ChatInterface component
import { useAuth } from '../contexts/AuthContext';

const FloatingChat = ({ isOpen, onClose, onOpen, onTaskUpdate }) => {
  const { token, user } = useAuth();

  if (!isOpen) {
    return (
      <button className="floating-chat-button" onClick={onOpen}>
        💬
      </button>
    );
  }

  return (
    <div className="floating-chat-container">
      <div className="floating-chat-header">
        <h3>AI Assistant</h3>
        <button className="close-chat-button" onClick={onClose}>×</button>
      </div>
      <ChatInterface onTaskUpdate={onTaskUpdate} />
    </div>
  );
};

export default FloatingChat;