// Orders and bookings are sent to Sherrif's WhatsApp (053 581 5707).
const WHATSAPP_NUMBER = "233535815707";

const DISHES = {
  waakye: "Hot & Spicy Waakye",
  jollof: "Jollof Rice",
  plain: "Plain Rice",
};

function openWhatsApp(message) {
  const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
  window.open(url, "_blank", "noopener");
}

// ---- Home: rotating food photos behind the hero ----
const slides = document.querySelectorAll(".hero-slides .slide");
if (slides.length) {
  const dots = document.querySelector(".hero-dots");
  let current = 0;
  let timer;

  const show = (i) => {
    slides[current].classList.remove("is-active");
    dots.children[current].setAttribute("aria-selected", "false");
    current = (i + slides.length) % slides.length;
    slides[current].classList.add("is-active");
    dots.children[current].setAttribute("aria-selected", "true");
  };
  const start = () => {
    clearInterval(timer);
    timer = setInterval(() => show(current + 1), 4000);
  };

  slides.forEach((_, i) => {
    const dot = document.createElement("button");
    dot.type = "button";
    dot.setAttribute("role", "tab");
    dot.setAttribute("aria-label", `Photo ${i + 1}`);
    dot.setAttribute("aria-selected", String(i === 0));
    dot.addEventListener("click", () => { show(i); start(); });
    dots.appendChild(dot);
  });

  start();
}

// ---- Menu: steppers, cart bar and checkout ----
const orderForm = document.getElementById("order-form");
if (orderForm) {
  const fields = orderForm.elements;
  const cart = { waakye: 0, jollof: 0, plain: 0 };
  const summary = document.getElementById("order-summary");
  const cartBar = document.getElementById("cart-bar");
  const cartCount = document.getElementById("cart-count");
  const orderError = document.getElementById("order-error");
  const addressField = document.getElementById("address-field");

  const render = () => {
    const items = Object.entries(cart).filter(([, qty]) => qty > 0);
    const total = items.reduce((sum, [, qty]) => sum + qty, 0);

    document.querySelectorAll(".stepper").forEach((s) => {
      s.querySelector("output").textContent = cart[s.dataset.dish];
    });
    summary.innerHTML = items.length
      ? items.map(([key, qty]) => `<li><span>${DISHES[key]}</span><span>× ${qty}</span></li>`).join("")
      : '<li class="muted">No dishes yet. Tap + on a dish above.</li>';
    cartCount.textContent = total;
    cartBar.hidden = total === 0;
  };

  document.querySelectorAll(".stepper").forEach((s) => {
    s.addEventListener("click", (e) => {
      const btn = e.target.closest("button");
      if (!btn) return;
      const dish = s.dataset.dish;
      cart[dish] = Math.max(0, Math.min(50, cart[dish] + Number(btn.dataset.step)));
      orderError.textContent = "";
      render();
    });
  });

  // Hide the floating cart bar once the checkout form is on screen.
  const checkout = document.getElementById("checkout");
  new IntersectionObserver(([entry]) => {
    cartBar.style.visibility = entry.isIntersecting ? "hidden" : "";
  }).observe(checkout);

  const updateAddressField = () => {
    const delivery = fields.method.value === "Delivery";
    addressField.hidden = !delivery;
    fields.address.required = delivery;
  };
  orderForm.querySelectorAll('input[name="method"]').forEach((r) =>
    r.addEventListener("change", updateAddressField)
  );
  updateAddressField();

  orderForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const items = Object.entries(cart).filter(([, qty]) => qty > 0);
    if (items.length === 0) {
      orderError.textContent = "Please add at least one dish.";
      document.getElementById("waakye").scrollIntoView({ behavior: "smooth" });
      return;
    }
    if (!orderForm.reportValidity()) return;
    orderError.textContent = "";

    const lines = [
      "Hello Sherrif's, I'd like to place an order:",
      "",
      ...items.map(([key, qty]) => `• ${qty} x ${DISHES[key]}`),
      "",
      fields.method.value,
      `Name: ${fields.name.value.trim()}`,
      `Phone: ${fields.phone.value.trim()}`,
    ];
    if (fields.method.value === "Delivery") lines.push(`Address: ${fields.address.value.trim()}`);
    if (fields.notes.value.trim()) lines.push(`Notes: ${fields.notes.value.trim()}`);

    openWhatsApp(lines.join("\n"));
  });

  render();
}

// ---- Book: catering booking ----
const bookForm = document.getElementById("book-form");
if (bookForm) {
  const fields = bookForm.elements;
  const bookError = document.getElementById("book-error");

  // Bookings can't be made for a date in the past.
  const today = new Date();
  today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
  fields.date.min = today.toISOString().split("T")[0];

  bookForm.addEventListener("submit", (e) => {
    e.preventDefault();
    bookError.textContent = "";

    if (!fields.event.value) {
      bookError.textContent = "Please choose the type of event.";
      return;
    }
    const dishes = [...bookForm.querySelectorAll('input[name="dishes"]:checked')].map((c) => c.value);
    if (dishes.length === 0) {
      bookError.textContent = "Please choose at least one dish.";
      return;
    }
    if (!bookForm.reportValidity()) return;

    const date = new Date(`${fields.date.value}T00:00`).toLocaleDateString("en-GB", {
      weekday: "long",
      day: "numeric",
      month: "long",
      year: "numeric",
    });
    const lines = [
      "Hello Sherrif's, I'd like to book you for an event:",
      "",
      `Event: ${fields.event.value}`,
      `Date: ${date}`,
      `Guests: ${fields.guests.value}`,
      `Dishes: ${dishes.join(", ")}`,
      `Location: ${fields.location.value.trim()}`,
      "",
      `Name: ${fields.name.value.trim()}`,
      `Phone: ${fields.phone.value.trim()}`,
    ];
    if (fields.notes.value.trim()) lines.push(`Notes: ${fields.notes.value.trim()}`);

    openWhatsApp(lines.join("\n"));
  });
}
