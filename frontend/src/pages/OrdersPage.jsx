import { useEffect, useState } from "react";

import Message from "../components/Message.jsx";
import { fetchCustomerOrders } from "../services/api.js";

function labelStatus(status) {
  return status.charAt(0).toUpperCase() + status.slice(1);
}

export default function OrdersPage({ auth }) {
  const [orders, setOrders] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadOrders() {
    setMessage("");
    setError("");

    if (!auth.token) {
      setError("Login as a customer to track orders.");
      return;
    }

    try {
      const data = await fetchCustomerOrders(auth.token);
      setOrders(data);
      setMessage("Order status refreshed.");
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadOrders();
  }, []);

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Order Tracking</h2>
        <button onClick={loadOrders}>Refresh</button>
      </div>
      <Message type="success">{message}</Message>
      <Message type="error">{error}</Message>

      {orders.length === 0 ? (
        <p className="empty">No customer orders found.</p>
      ) : (
        <div className="list">
          {orders.map((order) => (
            <article className="order" key={order.id}>
              <div className="order-header">
                <strong>Order #{order.id}</strong>
                <span className="status-badge">{labelStatus(order.status)}</span>
              </div>
              <p>
                Payment: {order.payment_status} via {order.payment_method}
              </p>
              <p>Total: {order.total.toFixed(2)} EGP</p>
              <ul>
                {order.items.map((item) => (
                  <li key={`${order.id}-${item.name}`}>
                    {item.quantity} x {item.name} - {item.line_total.toFixed(2)} EGP
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
