import { useMemo, useState } from "react";

import Navigation from "./components/Navigation.jsx";
import CartPage from "./pages/CartPage.jsx";
import KitchenDashboardPage from "./pages/KitchenDashboardPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import MenuPage from "./pages/MenuPage.jsx";
import OrdersPage from "./pages/OrdersPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";

const storedToken = localStorage.getItem("access_token") || "";
const storedRole = localStorage.getItem("role") || "";

export default function App() {
  const [page, setPage] = useState(storedToken ? "menu" : "login");
  const [auth, setAuth] = useState({ token: storedToken, role: storedRole });
  const [cart, setCart] = useState([]);

  const cartCount = useMemo(
    () => cart.reduce((sum, item) => sum + item.quantity, 0),
    [cart],
  );

  function handleLogin(session) {
    localStorage.setItem("access_token", session.access_token);
    localStorage.setItem("role", session.role);
    setAuth({ token: session.access_token, role: session.role });
    setPage(session.role === "kitchen" ? "kitchen" : "menu");
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    setAuth({ token: "", role: "" });
    setPage("login");
  }

  function addToCart(item, quantity) {
    setCart((current) => {
      const existing = current.find((cartItem) => cartItem.id === item.id);
      if (!existing) {
        return [...current, { ...item, quantity }];
      }
      return current.map((cartItem) =>
        cartItem.id === item.id
          ? { ...cartItem, quantity: Math.min(10, cartItem.quantity + quantity) }
          : cartItem,
      );
    });
  }

  function removeFromCart(itemId) {
    setCart((current) => current.filter((item) => item.id !== itemId));
  }

  function renderPage() {
    if (page === "register") {
      return <RegisterPage />;
    }
    if (page === "login") {
      return <LoginPage onLogin={handleLogin} />;
    }
    if (page === "cart") {
      return (
        <CartPage
          auth={auth}
          cart={cart}
          onRemoveItem={removeFromCart}
          onClearCart={() => setCart([])}
          onOrderPlaced={() => setPage("orders")}
        />
      );
    }
    if (page === "orders") {
      return <OrdersPage auth={auth} />;
    }
    if (page === "kitchen") {
      return <KitchenDashboardPage auth={auth} />;
    }
    return <MenuPage onAddToCart={addToCart} />;
  }

  return (
    <>
      <Navigation
        page={page}
        setPage={setPage}
        auth={auth}
        cartCount={cartCount}
        onLogout={handleLogout}
      />
      <main>{renderPage()}</main>
    </>
  );
}
