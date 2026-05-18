import { useState } from "react";

import Message from "../components/Message.jsx";
import { fetchKitchenOrders, updateOrderStatus } from "../services/api.js";

const STATUSES = ["pending", "preparing", "ready", "completed"];

export default function KitchenDashboardPage({ auth }) {
  const [orders, setOrders] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadOrders() {
    setMessage("");
    setError("");

    if (!auth.token) {
      setError("Login as kitchen staff to view orders.");
      return;
    }

    try {
      const data = await fetchKitchenOrders(auth.token);
      setOrders(data);
      setMessage("Kitchen orders loaded.");
    } catch (err) {
      setError(err.message);
    }
  }

  async function changeStatus(orderId, status) {
    setMessage("");
    setError("");

    try {
      await updateOrderStatus(auth.token, orderId, status);
      setOrders((current) =>
        current.map((order) => (order.id === orderId ? { ...order, status } : order)),
      );
      setMessage(`Order #${orderId} updated to ${status}.`);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Kitchen Dashboard</h2>
        <button onClick={loadOrders}>Load orders</button>
      </div>
      <Message type="success">{message}</Message>
      <Message type="error">{error}</Message>

      {orders.length === 0 ? (
        <p className="empty">No orders loaded.</p>
      ) : (
        <div className="list">
          {orders.map((order) => (
            <article className="order" key={order.id}>
              <div className="order-header">
                <strong>Order #{order.id}</strong>
                <span>{order.status}</span>
              </div>
              <p>{order.customer_email}</p>
              <p>
                Payment: {order.payment_status} via {order.payment_method}
              </p>
              <ul>
                {order.items.map((item) => (
                  <li key={`${order.id}-${item.name}`}>
                    {item.quantity} x {item.name}
                  </li>
                ))}
              </ul>
              <label>
                Status
                <select
                  value={order.status}
                  onChange={(event) => changeStatus(order.id, event.target.value)}
                >
                  {STATUSES.map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
              </label>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
