import React, { useState } from "react";
import "../App.css";

const API_URL = "http://127.0.0.1:8000/api/ask-yojanalm";

function YojanaLM() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [language, setLanguage] = useState("English");
  const [loading, setLoading] = useState(false);

  // Keep the same profile structure used by your backend.
  // If your application already stores the profile elsewhere,
  // you can replace this with that profile source.
  const profile = {
    age: 21,
    state: "Andhra Pradesh",
    occupation: "Student",
    income: 300000,
    gender: "Male",
    social_category: "General",
  };

  const handleSend = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          profile: profile,
          question: trimmedQuestion,
          language: language,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();

      let answer = data.answer;

      // Some backend responses may return the answer
      // inside a stringified Python/JSON object.
      if (typeof answer === "object" && answer !== null) {
        answer =
          answer.answer ||
          answer.response ||
          answer.message ||
          JSON.stringify(answer);
      }

      if (!answer) {
        answer = "I couldn't generate an answer for that question.";
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: String(answer),
        },
      ]);
    } catch (error) {
      console.error("YojanaLM error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to YojanaLM right now. Please make sure the backend server is running.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleSuggestion = (text) => {
    setQuestion(text);
  };

  return (
    <div className="yojanalm-page">
      <div className="yojanalm-container">

        {/* Header */}
        <div className="yojanalm-heading">
          <div className="yojanalm-eyebrow">
            YOJANALM ASSISTANT
          </div>

          <h1>Ask YojanaLM</h1>

          <p>
            Ask about government schemes, eligibility, benefits and
            applications.
          </p>
        </div>

        {/* Chat Card */}
        <div className="yojanalm-chat-card">

          {/* Top bar */}
          <div className="yojanalm-topbar">
            <div className="yojanalm-model-info">
              <div className="yojanalm-model-dot"></div>

              <div>
                <div className="yojanalm-model-name">
                  YojanaLM
                </div>

                <div className="yojanalm-model-status">
                  Government scheme assistant
                </div>
              </div>
            </div>

            <div className="yojanalm-language">
              <label htmlFor="language">
                Response Language
              </label>

              <select
                id="language"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                <option value="English">English</option>
              </select>
            </div>
          </div>

          {/* Messages */}
          <div className="yojanalm-messages">

            {messages.length === 0 ? (
              <div className="yojanalm-empty">

                <div className="yojanalm-empty-icon">
                  ✦
                </div>

                <h2>How can I help you?</h2>

                <p>
                  Ask about government schemes, eligibility,
                  benefits or applications.
                </p>

                <div className="yojanalm-profile-note">
                  YojanaLM provides personalized answers based on
                  your profile.
                </div>

                <div className="yojanalm-suggestions">

                  <button
                    onClick={() =>
                      handleSuggestion(
                        "What government schemes are available for me?"
                      )
                    }
                  >
                    Find schemes for me
                  </button>

                  <button
                    onClick={() =>
                      handleSuggestion(
                        "What are the benefits of PM-KISAN?"
                      )
                    }
                  >
                    Ask about benefits
                  </button>

                  <button
                    onClick={() =>
                      handleSuggestion(
                        "What documents are required for PM-KISAN?"
                      )
                    }
                  >
                    Check documents
                  </button>

                </div>
              </div>
            ) : (
              <div className="yojanalm-conversation">

                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`yojanalm-message-row ${
                      message.role === "user"
                        ? "user-row"
                        : "assistant-row"
                    }`}
                  >

                    {message.role === "assistant" && (
                      <div className="yojanalm-avatar">
                        ✦
                      </div>
                    )}

                    <div
                      className={`yojanalm-message ${
                        message.role === "user"
                          ? "user-message"
                          : "assistant-message"
                      } ${
                        message.error
                          ? "error-message"
                          : ""
                      }`}
                    >
                      {message.content
                        .split("\n")
                        .map((line, lineIndex) => (
                          <React.Fragment key={lineIndex}>
                            {line}
                            {lineIndex <
                              message.content.split("\n").length - 1 && (
                              <br />
                            )}
                          </React.Fragment>
                        ))}
                    </div>

                  </div>
                ))}

                {loading && (
                  <div className="yojanalm-message-row assistant-row">

                    <div className="yojanalm-avatar">
                      ✦
                    </div>

                    <div className="yojanalm-message assistant-message loading-message">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>

                  </div>
                )}

              </div>
            )}
          </div>

          {/* Input area */}
          <div className="yojanalm-input-section">

            <div className="yojanalm-input-wrapper">

              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask YojanaLM about a government scheme..."
                rows="1"
                disabled={loading}
              />

              <button
                className="yojanalm-send-button"
                onClick={handleSend}
                disabled={!question.trim() || loading}
              >
                {loading ? "..." : "Send"}
              </button>

            </div>

            <div className="yojanalm-input-hint">
              Press Enter to send
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}

export default YojanaLM;