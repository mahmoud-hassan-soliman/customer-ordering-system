import { useEffect, useState } from "react";

import Message from "../components/Message.jsx";
import { fetchMenu } from "../services/api.js";

export default function MenuPage({ onAddToCart }) {
  const [items, setItems] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchMenu()
      .then((menu) => {
        setItems(menu);
        setError("");
      })
      .catch((err) => setError(err.message));
  }, []);

  function quantityFor(itemId) {
    return quantities[itemId] || 1;
  }

  function setQuantity(itemId, value) {
    setQuantities({ ...quantities, [itemId]: Number(value) });
  }

  function addItem(item) {
    const quantity = quantityFor(item.id);
    if (quantity < 1 || quantity > 10) {
      setError("Quantity must be between 1 and 10.");
      return;
    }
    onAddToCart(item, quantity);
    setMessage(`${item.name} added to cart.`);
    setError("");
  }

  return (
    <section className="panel">
      <h2>Menu</h2>
      <Message type="success">{message}</Message>
      <Message type="error">{error}</Message>
      <div className="list">
        {items.map((item) => (
          <article className="row" key={item.id}>
            <div>
              <strong>{item.name}</strong>
              <span>{item.price.toFixed(2)} EGP</span>
            </div>
            <label>
              Qty
              <input
                type="number"
                min="1"
                max="10"
                value={quantityFor(item.id)}
                onChange={(event) => setQuantity(item.id, event.target.value)}
              />
            </label>
            <button onClick={() => addItem(item)}>Add</button>
          </article>
        ))}
      </div>
    </section>
  );
}

