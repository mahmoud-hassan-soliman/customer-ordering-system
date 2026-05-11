import { useState } from "react";

import Message from "../components/Message.jsx";
import { registerUser } from "../services/api.js";

export default function RegisterPage() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "customer",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  function updateField(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage("");
    setError("");

    try {
      const user = await registerUser(form);
      setMessage(`Registered ${user.email}. You can log in now.`);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="panel">
      <h2>Register</h2>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Name
          <input name="name" value={form.name} onChange={updateField} required />
        </label>
        <label>
          Email
          <input name="email" type="email" value={form.email} onChange={updateField} required />
        </label>
        <label>
          Password
          <input
            name="password"
            type="password"
            minLength={8}
            value={form.password}
            onChange={updateField}
            required
          />
        </label>
        <label>
          Role
          <select name="role" value={form.role} onChange={updateField}>
            <option value="customer">Customer</option>
            <option value="kitchen">Kitchen</option>
          </select>
        </label>
        <button type="submit">Create account</button>
      </form>
      <Message type="success">{message}</Message>
      <Message type="error">{error}</Message>
    </section>
  );
}

