import { useState } from "react";

import Message from "../components/Message.jsx";
import { loginUser } from "../services/api.js";

export default function LoginPage({ onLogin }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  function updateField(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    try {
      const session = await loginUser(form);
      onLogin(session);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="panel">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Email
          <input name="email" type="email" value={form.email} onChange={updateField} required />
        </label>
        <label>
          Password
          <input name="password" type="password" value={form.password} onChange={updateField} required />
        </label>
        <button type="submit">Login</button>
      </form>
      <Message type="error">{error}</Message>
    </section>
  );
}

