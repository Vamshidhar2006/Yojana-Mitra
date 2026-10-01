import { useState } from "react";
import axios from "axios";

function Chat() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    // Language belongs only to the chatbot
    const [language, setLanguage] = useState("English");

    function handleLanguageChange(event) {
        setLanguage(event.target.value);
    }

    async function handleSubmit(event) {
        event.preventDefault();

        if (!question.trim() || loading) {
            return;
        }

        const userQuestion = question.trim();

        // Add user message
        setMessages((previousMessages) => [
            ...previousMessages,
            {
                type: "user",
                text: userQuestion
            }
        ]);

        setQuestion("");
        setLoading(true);

        try {
            const savedProfile =
                localStorage.getItem("yojanaProfile");

            if (!savedProfile) {
                setMessages((previousMessages) => [
                    ...previousMessages,
                    {
                        type: "assistant",
                        text:
                            "Please set up your profile first so I can give you personalized government scheme information."
                    }
                ]);

                setLoading(false);
                return;
            }

            const profile = JSON.parse(savedProfile);

            const response = await axios.post(
                "http://127.0.0.1:8000/api/ask",
                {
                    profile: profile,
                    question: userQuestion,
                    language: language
                }
            );

            setMessages((previousMessages) => [
                ...previousMessages,
                {
                    type: "assistant",
                    text: response.data.answer
                }
            ]);
        } catch (error) {
            console.error(
                "Error asking Yojana Mitra:",
                error
            );

            setMessages((previousMessages) => [
                ...previousMessages,
                {
                    type: "assistant",
                    text:
                        "Sorry, I couldn't get an answer right now. Please try again."
                }
            ]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="chat-page">

            <div className="chat-heading">
                <p className="small-title">
                    YOJANA MITRA ASSISTANT
                </p>

                <h1>Ask Yojana Mitra</h1>

                <p>
                    Ask about government schemes,
                    eligibility, benefits and applications.
                </p>
            </div>

            <div className="chat-box">

                {/* Language selector only inside chatbot */}
                <div className="chat-language">
                    <label htmlFor="chat-language">
                        Response Language
                    </label>

                    <select
                        id="chat-language"
                        value={language}
                        onChange={handleLanguageChange}
                    >
                        <option value="English">
                            English
                        </option>

                        <option value="Hindi">
                            Hindi
                        </option>

                        <option value="Telugu">
                            Telugu
                        </option>

                        <option value="Tamil">
                            Tamil
                        </option>

                        <option value="Kannada">
                            Kannada
                        </option>

                        <option value="Malayalam">
                            Malayalam
                        </option>

                        <option value="Marathi">
                            Marathi
                        </option>

                        <option value="Gujarati">
                            Gujarati
                        </option>

                        <option value="Bengali">
                            Bengali
                        </option>

                        <option value="Odia">
                            Odia
                        </option>
                    </select>
                </div>

                <div className="messages">

                    {messages.length === 0 && (
                        <div className="welcome-message">
                            <h3>
                                How can I help you?
                            </h3>

                            <p>
                                Ask about government
                                schemes, eligibility,
                                benefits or applications.
                            </p>

                            <p>
                                Response language:{" "}
                                <strong>
                                    {language}
                                </strong>
                            </p>
                        </div>
                    )}

                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`message ${message.type}`}
                        >
                            {message.text}
                        </div>
                    ))}

                    {loading && (
                        <div className="message assistant">
                            Yojana Mitra is thinking...
                        </div>
                    )}

                </div>

                <form
                    className="chat-input"
                    onSubmit={handleSubmit}
                >
                    <input
                        type="text"
                        value={question}
                        onChange={(event) =>
                            setQuestion(event.target.value)
                        }
                        placeholder="Ask about a government scheme..."
                        disabled={loading}
                    />

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? "..." : "Send"}
                    </button>
                </form>

            </div>
        </div>
    );
}

export default Chat;