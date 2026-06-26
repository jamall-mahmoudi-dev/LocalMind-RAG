import React, { useState } from "react";
import axios from "axios";
import DocumentUpload from "./components/DocumentUpload.jsx";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/query/`, { question });
      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 640, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>RAG Chat</h1>
      <textarea
        rows={3}
        style={{ width: "100%" }}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something about your documents..."
      />
      <button onClick={ask} disabled={loading || !question}>
        {loading ? "Thinking..." : "Ask"}
      </button>
      {answer && (
        <div style={{ marginTop: 20, whiteSpace: "pre-wrap" }}>{answer}</div>
      )}
      <DocumentUpload />
    </div>
  );
}
