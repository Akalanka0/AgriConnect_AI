import { useRef, useEffect } from "react";
import { Send, Loader2, Sun, Moon, RotateCcw } from "lucide-react";
import { useChat } from "../hooks/useChat.js";
import { useTheme } from "../hooks/useTheme.js";
import { SUGGESTED_QUESTIONS } from "../utils/constants.js";

/* ── Typing dots ──────────────────────────────────────────────────────────── */
function TypingDots() {
  return (
    <div className="flex items-center gap-1.5 py-0.5">
      <span className="typing-dot" />
      <span className="typing-dot" />
      <span className="typing-dot" />
    </div>
  );
}

/* ── Welcome screen ───────────────────────────────────────────────────────── */
function WelcomeScreen({ setQuestion }) {
  return (
    <div className="flex flex-col items-center justify-center h-full px-6 py-8 animate-fadeIn">
      {/* Icon */}
      <div className="w-14 h-14 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg shadow-emerald-200/50 dark:shadow-emerald-900/50 mb-4">
        <i className="fas fa-seedling text-2xl text-white" />
      </div>

      <h2 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-1 text-center">
        AgriConnect AI
      </h2>
      <p className="text-gray-400 dark:text-gray-500 text-sm text-center mb-8 max-w-[220px] leading-relaxed">
        Ask anything about farming, crops, or agriculture
      </p>

      {/* Suggestion chips — no emoji */}
      <div className="flex flex-wrap gap-2 justify-center">
        {SUGGESTED_QUESTIONS.map((q) => (
          <button
            key={q}
            onClick={() => setQuestion(q)}
            className="suggestion-chip"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}

/* ── Single message bubble ────────────────────────────────────────────────── */
function MessageBubble({ msg, formatTime }) {
  const isUser = msg.sender === "user";

  return (
    <div
      className={`flex gap-2.5 ${isUser ? "flex-row-reverse" : ""} animate-fadeIn`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 mt-1 w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-bold ${
          isUser
            ? "bg-emerald-500 text-white"
            : "bg-white dark:bg-gray-700 border border-emerald-100 dark:border-emerald-800 text-emerald-600 dark:text-emerald-400"
        }`}
      >
        {isUser ? "You" : <i className="fas fa-seedling text-[11px]" />}
      </div>

      {/* Content */}
      <div
        className={`flex flex-col gap-1 max-w-[78%] ${
          isUser ? "items-end" : "items-start"
        }`}
      >
        {/* Bubble */}
        <div
          className={`px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? "bg-emerald-500 text-white rounded-tr-sm"
              : "bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 border border-gray-100 dark:border-gray-600 shadow-sm rounded-tl-sm"
          }`}
        >
          <p className="whitespace-pre-wrap">{msg.text}</p>
        </div>

        {/* Timestamp */}
        {msg.timestamp && (
          <span className="text-[10px] text-gray-400 dark:text-gray-500 px-0.5">
            {formatTime(msg.timestamp)}
          </span>
        )}
      </div>
    </div>
  );
}

/* ── Main Chat component ──────────────────────────────────────────────────── */
function Chat() {
  const {
    question,
    setQuestion,
    messages,
    loading,
    error,
    messagesEndRef,
    askAI,
    handleKeyDown,
    clearChat,
  } = useChat();

  const { isDark, toggleTheme } = useTheme();
  const textareaRef = useRef(null);

  /* Auto-grow textarea */
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 100) + "px";
  }, [question]);

  const formatTime = (ts) =>
    ts
      ? new Date(ts).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        })
      : "";

  return (
    /* ── Page background ──────────────────────────────────────────────────── */
    <div className="min-h-screen flex items-center justify-center p-0 sm:p-6 bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-gray-950 dark:via-slate-900 dark:to-gray-950 transition-colors duration-300">
      {/* ── Chat card ───────────────────────────────────────────────────────── */}
      <div className="w-full sm:max-w-[480px] h-screen sm:h-[640px] flex flex-col bg-white dark:bg-gray-900 sm:rounded-2xl sm:shadow-2xl overflow-hidden border-0 sm:border sm:border-gray-100 dark:sm:border-gray-800 transition-colors duration-300">
        {/* ── Minimal toolbar ─────────────────────────────────────────────── */}
        <div className="flex-shrink-0 flex items-center justify-end gap-1 px-3 py-2 border-b border-gray-100 dark:border-gray-800">
          {/* Reset — only visible when a conversation is active */}
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              title="New conversation"
              className="toolbar-btn"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          )}

          {/* Theme toggle */}
          <button
            onClick={toggleTheme}
            title={isDark ? "Light mode" : "Dark mode"}
            className="toolbar-btn"
          >
            {isDark ? (
              <Sun className="w-3.5 h-3.5" />
            ) : (
              <Moon className="w-3.5 h-3.5" />
            )}
          </button>
        </div>

        {/* ── Messages ────────────────────────────────────────────────────── */}
        <main className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <WelcomeScreen setQuestion={setQuestion} />
          ) : (
            <div className="px-4 py-4 space-y-4">
              {messages.map((msg, i) => (
                <MessageBubble key={i} msg={msg} formatTime={formatTime} />
              ))}

              {/* Typing indicator */}
              {loading && (
                <div className="flex gap-2.5 animate-fadeIn">
                  <div className="flex-shrink-0 mt-1 w-7 h-7 rounded-full bg-white dark:bg-gray-700 border border-emerald-100 dark:border-emerald-800 flex items-center justify-center">
                    <i className="fas fa-seedling text-[11px] text-emerald-500 dark:text-emerald-400" />
                  </div>
                  <div className="bg-white dark:bg-gray-700 border border-gray-100 dark:border-gray-600 shadow-sm rounded-2xl rounded-tl-sm px-3.5 py-2.5">
                    <TypingDots />
                  </div>
                </div>
              )}

              {/* Error */}
              {error && (
                <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-300 rounded-xl px-3 py-2.5 text-xs text-center animate-fadeIn">
                  ⚠️ {error}
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}
        </main>

        {/* ── Input ───────────────────────────────────────────────────────── */}
        <footer className="flex-shrink-0 border-t border-gray-100 dark:border-gray-800 px-3 py-3 bg-white dark:bg-gray-900 transition-colors duration-300">
          <div className="flex items-end gap-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 transition-all duration-200 focus-within:border-emerald-400 dark:focus-within:border-emerald-600 focus-within:ring-2 focus-within:ring-emerald-100 dark:focus-within:ring-emerald-900/40 focus-within:bg-white dark:focus-within:bg-gray-800">
            <textarea
              ref={textareaRef}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about crops, farming…"
              disabled={loading}
              rows={1}
              className="flex-1 bg-transparent text-sm text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 resize-none outline-none no-scrollbar leading-relaxed py-0.5"
              style={{ maxHeight: "100px", minHeight: "20px" }}
            />
            <button
              onClick={askAI}
              disabled={loading || !question.trim()}
              className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-lg send-btn"
            >
              {loading ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <Send className="w-3.5 h-3.5" />
              )}
            </button>
          </div>

          <p className="text-center text-[10px] text-gray-400 dark:text-gray-600 mt-1.5 select-none">
            <kbd className="kbd">Enter</kbd> to send ·{" "}
            <kbd className="kbd">Shift+Enter</kbd> for new line
          </p>
        </footer>
      </div>
    </div>
  );
}

export default Chat;
