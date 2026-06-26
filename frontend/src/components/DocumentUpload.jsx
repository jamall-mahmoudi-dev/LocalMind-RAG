import React, { useEffect, useState } from "react";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export default function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);

  const fetchDocuments = async () => {
    const res = await axios.get(`${API_BASE_URL}/documents/`);
    setDocuments(res.data.results || res.data);
  };

  useEffect(() => {
    fetchDocuments();
    const interval = setInterval(fetchDocuments, 5000);
    return () => clearInterval(interval);
  }, []);

  const upload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", file.name);
    try {
      await axios.post(`${API_BASE_URL}/documents/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFile(null);
      fetchDocuments();
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ marginTop: 32 }}>
      <h2>Documents</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload} disabled={!file || uploading}>
        {uploading ? "Uploading..." : "Upload"}
      </button>

      <ul>
        {documents.map((doc) => (
          <li key={doc.id}>
            {doc.title} — <strong>{doc.status}</strong>
            {doc.status === "ready" && ` (${doc.chunk_count} chunks)`}
            {doc.status === "failed" && ` (${doc.error_message})`}
          </li>
        ))}
      </ul>
    </div>
  );
}
