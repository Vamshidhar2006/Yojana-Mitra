
import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../App.css";
import API_BASE_URL from "../services/api";
const API_URL = `${API_BASE_URL}/api/ask-yojanalm`;



function YojanaLM() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [language, setLanguage] = useState("English");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) return;

    // Read the latest profile saved by the existing profile form.
    let profile;

    try {
      const savedProfile = localStorage.getItem("yojanaProfile");
      profile = savedProfile ? JSON.parse(savedProfile) : null;
    } catch (error) {
      console.error("Error reading saved profile:", error);
      profile = null;
    }

    // Require a saved profile before sending the question.
    if (!profile) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Please set up your profile before asking questions so I can personalize your scheme recommendations.",
          needsProfile: true,
        },
      ]);
      setQuestion("");
      return;
    }

    const requiredFields = [
      "age",
      "state",
      "occupation",
      "income",
      "gender",
      "social_category",
    ];

    const hasMissingFields = requiredFields.some(
      (field) =>
        profile[field] === undefined ||
        profile[field] === null ||
        String(profile[field]).trim() === ""
    );

    if (hasMissingFields) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Your profile is incomplete. Please edit and save it before continuing.",
          needsProfile: true,
        },
      ]);
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
          profile: {
            age: Number(profile.age),
            state: profile.state,
            occupation: profile.occupation,
            income: Number(profile.income),
            gender: profile.gender,
            social_category: profile.social_category,
          },
          question: trimmedQuestion,
          language,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      let answer = data.answer;

      if (typeof answer === "object" && answer !== null) {
        answer =
          answer.answer ||
          answer.response ||
          answer.message ||
          JSON.stringify(answer, null, 2);
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
            "Sorry, I couldn't connect to YojanaLM. Please check whether the backend server is running.",
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

        <div className="yojanalm-chat-card">
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
                onChange={(event) => setLanguage(event.target.value)}
              >
                <option value="English">English</option>
              </select>
            </div>
          </div>

          <div className="yojanalm-messages">
            {messages.length === 0 ? (
              <div className="yojanalm-empty">
                <div className="yojanalm-empty-icon">✦</div>

                <h2>How can I help you?</h2>

                <p>
                  Ask about government schemes, eligibility,
                  benefits or applications.
                </p>

                <div className="yojanalm-profile-note">
                  Answers use your saved Yojana Mitra profile.
                </div>

                <div className="yojanalm-suggestions">
                  <button
                    type="button"
                    onClick={() =>
                      handleSuggestion(
                        "What government schemes are available for me?"
                      )
                    }
                  >
                    Find schemes for me
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      handleSuggestion(
                        "What are the benefits of PM-KISAN?"
                      )
                    }
                  >
                    Ask about benefits
                  </button>

                  <button
                    type="button"
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
                      <div className="yojanalm-avatar">✦</div>
                    )}

                    <div
                      className={`yojanalm-message ${
                        message.role === "user"
                          ? "user-message"
                          : "assistant-message"
                      } ${message.error ? "error-message" : ""}`}
                    >
                      {message.content.split("\n").map((line, lineIndex, lines) => (
                        <React.Fragment key={lineIndex}>
                          {line}
                          {lineIndex < lines.length - 1 && <br />}
                        </React.Fragment>
                      ))}

                      {message.needsProfile && (
                        <div style={{ marginTop: "12px" }}>
                          <Link to="/profile-setup">
                            <button
                              type="button"
                              className="primary-button"
                            >
                              Set Up / Edit Profile
                            </button>
                          </Link>
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="yojanalm-message-row assistant-row">
                    <div className="yojanalm-avatar">✦</div>

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

          <div className="yojanalm-input-section">
            <div className="yojanalm-input-wrapper">
              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask YojanaLM about a government scheme..."
                rows="1"
                disabled={loading}
              />

              <button
                type="button"
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
