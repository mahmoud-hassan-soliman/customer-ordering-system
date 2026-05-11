export default function Navigation({ page, setPage, auth, cartCount, onLogout }) {
  return (
    <header className="topbar">
      <div>
        <h1>Customer Ordering System</h1>
        <p>Small ordering demo</p>
      </div>
      <nav aria-label="Main navigation">
        <button className={page === "register" ? "active" : ""} onClick={() => setPage("register")}>
          Register
        </button>
        <button className={page === "login" ? "active" : ""} onClick={() => setPage("login")}>
          Login
        </button>
        <button className={page === "menu" ? "active" : ""} onClick={() => setPage("menu")}>
          Menu
        </button>
        <button className={page === "cart" ? "active" : ""} onClick={() => setPage("cart")}>
          Cart ({cartCount})
        </button>
        <button className={page === "kitchen" ? "active" : ""} onClick={() => setPage("kitchen")}>
          Kitchen
        </button>
      </nav>
      <div className="session">
        {auth.token ? (
          <>
            <span>{auth.role}</span>
            <button onClick={onLogout}>Logout</button>
          </>
        ) : (
          <span>Not logged in</span>
        )}
      </div>
    </header>
  );
}

