import { useState } from "react";

import Message from "../components/Message.jsx";
import { placeOrder } from "../services/api.js";

export default function CartPage({ auth, cart, onRemoveItem, onClearCart, onOrderPlaced }) {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const [paymentConfirmed, setPaymentConfirmed] = useState(false);

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  async function submitOrder() {
    setMessage("");
    setError("");

    if (!auth.token) {
      setError("Login as a customer before placing an order.");
      return;
    }

    try {
      const order = await placeOrder(auth.token, {
        client_order_key: `order-${Date.now()}-${Math.random().toString(16).slice(2)}`,
        payment_method: paymentMethod,
        payment_status: paymentConfirmed ? "paid" : "unpaid",
        items: cart.map((item) => ({
          menu_item_id: item.id,
          quantity: item.quantity,
        })),
      });
      onClearCart();
      setPaymentConfirmed(false);
      setMessage(
        `Order #${order.id} placed with status ${order.status}. Payment: ${order.payment_status}.`,
      );
      onOrderPlaced?.();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="panel">
      <h2>Cart</h2>
      <Message type="success">{message}</Message>
      <Message type="error">{error}</Message>

      {cart.length === 0 ? (
        <p className="empty">Cart is empty.</p>
      ) : (
        <div className="list">
          {cart.map((item) => (
            <article className="row" key={item.id}>
              <div>
                <strong>{item.name}</strong>
                <span>
                  {item.quantity} x {item.price.toFixed(2)} EGP
                </span>
              </div>
              <button onClick={() => onRemoveItem(item.id)}>Remove</button>
            </article>
          ))}
          <p className="total">Total: {total.toFixed(2)} EGP</p>
          <div className="payment-box">
            <label>
              Payment method
              <select
                value={paymentMethod}
                onChange={(event) => setPaymentMethod(event.target.value)}
              >
                <option value="cash">Cash</option>
                <option value="card">Card</option>
                <option value="wallet">Wallet</option>
              </select>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={paymentConfirmed}
                onChange={(event) => setPaymentConfirmed(event.target.checked)}
              />
              Confirm mock payment
            </label>
          </div>
        </div>
      )}

      <button onClick={submitOrder}>Place order</button>
    </section>
  );
}
