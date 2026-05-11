const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    throw new Error(body?.detail || `Request failed with status ${response.status}`);
  }

  return body;
}

function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function registerUser(payload) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function loginUser(payload) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchMenu() {
  return request("/menu");
}

export function placeOrder(token, payload) {
  return request("/orders", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
}

export function fetchKitchenOrders(token) {
  return request("/orders/kitchen", {
    headers: authHeaders(token),
  });
}

export function updateOrderStatus(token, orderId, status) {
  return request(`/orders/${orderId}/status`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify({ status }),
  });
}

