import { useState, useRef, useEffect } from "react";
import { TYPING_INDICATORS, API_BASE_URL } from "../utils/constants.js";

export const useChat = () => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [typingIndicator, setTypingIndicator] = useState("");
  const [conversationId, setConversationId] = useState(() =>
    crypto.randomUUID(),
  );
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (loading) {
      const randomIndicator =
        TYPING_INDICATORS[Math.floor(Math.random() * TYPING_INDICATORS.length)];
      setTypingIndicator(randomIndicator);
    } else {
      setTypingIndicator("");
    }
  }, [loading]);

  const askAI = async () => {
    if (!question.trim()) return;
    setError("");
    setLoading(true);
    const userMessage = {
      sender: "user",
      text: question,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question, conversation_id: conversationId }),
      });
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      const data = await response.json();

      // Keep the conversation_id in sync with whatever the backend assigned
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      const aiMessage = {
        sender: "ai",
        text: data.answer,
        sources: data.sources,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setQuestion("");
    } catch (err) {
      console.error("Backend error:", err);
      if (err instanceof TypeError && err.message.includes("fetch")) {
        setError(
          "Cannot reach the backend. Make sure the server is running on port 8000.",
        );
      } else if (err.message?.startsWith("Server error:")) {
        setError(
          `Server returned an error (${err.message}). Check the backend logs.`,
        );
      } else {
        setError("Failed to get a response. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askAI();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setQuestion("");
    setError("");
    setTypingIndicator("");
    // Generate a fresh conversation ID so the next session starts clean in Redis
    setConversationId(crypto.randomUUID());
  };

  return {
    question,
    setQuestion,
    messages,
    loading,
    error,
    typingIndicator,
    messagesEndRef,
    askAI,
    handleKeyDown,
    clearChat,
    conversationId,
  };
};
