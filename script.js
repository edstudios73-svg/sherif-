const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

// ---------- Mobile menu ----------
const menuBtn = $(".menu-btn");
const nav = $("#nav");
function setMenu(open) {
  nav.classList.toggle("open", open);
  menuBtn.setAttribute("aria-expanded", String(open));
  menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
}
menuBtn.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
nav.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

// ---------- Phone tab bar: mark the current page ----------
const here = location.pathname.split("/").pop() || "index.html";
$$(".tabbar a").forEach((a) => {
  if (a.getAttribute("href").split("#")[0] === here) a.classList.add("current");
});

// ---------- Service times: highlight today (Ghana time = UTC) ----------
const today = new Date().getUTCDay();
$$(".times").forEach((table) => {
  const note = table.nextElementSibling;
  const rows = $$(".times-row[data-day]", table);
  const row = rows.find((r) => Number(r.dataset.day) === today);
  const txt = (r, c) => $(c, r).textContent;
  if (row) {
    row.classList.add("is-today");
    note.textContent = `There's a meeting today: ${txt(row, ".t-name")}, ${txt(row, ".t-time")}. We'd love to see you.`;
  } else {
    const next = rows
      .map((r) => ({ r, d: (Number(r.dataset.day) - today + 7) % 7 }))
      .sort((a, b) => a.d - b.d)[0].r;
    note.textContent = `Next meeting: ${txt(next, ".t-day")}, ${txt(next, ".t-name")} at ${txt(next, ".t-time")}.`;
  }
  if (note && note.classList.contains("today-note")) note.hidden = false;
});

// ---------- At His Feet countdown ----------
// Friday 4 December 2026, 8:00 PM Ghana time (GMT, UTC+0). All night.
const START = new Date("2026-12-04T20:00:00Z");
const END = new Date("2026-12-05T05:00:00Z");
const cd = $("#countdown");
if (cd) {
  const cdMsg = $("#countdown-msg");
  const cells = Object.fromEntries($$("[data-u]", cd).map((el) => [el.dataset.u, el]));
  const pad = (n) => String(n).padStart(2, "0");
  let timer;
  const tick = () => {
    const now = new Date();
    if (now >= START) {
      cd.hidden = true;
      cdMsg.hidden = false;
      cdMsg.textContent = now >= END
        ? "Thank you to everyone who worshipped with us. Watch this space for the next service."
        : "Happening now. Come and worship with us all night.";
      clearInterval(timer);
      return;
    }
    const s = Math.floor((START - now) / 1000);
    cells.d.textContent = Math.floor(s / 86400);
    cells.h.textContent = pad(Math.floor((s % 86400) / 3600));
    cells.m.textContent = pad(Math.floor((s % 3600) / 60));
    cells.s.textContent = pad(s % 60);
  };
  tick();
  timer = setInterval(tick, 1000);
}

// ---------- Add to calendar (.ics) ----------
const cal = $("#add-calendar");
if (cal) {
  const fmt = (d) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  const ics = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//FDMI//At His Feet//EN",
    "BEGIN:VEVENT", "UID:at-his-feet-2026@fdmi",
    `DTSTAMP:${fmt(new Date())}`, `DTSTART:${fmt(START)}`, `DTEND:${fmt(END)}`,
    "SUMMARY:At His Feet: Worship All Night (FDMI)",
    "LOCATION:Church premises\\, last stop Adjen-Kotoku\\, next to Pick N Nikki School\\, Accra",
    "DESCRIPTION:Info: +233 59 470 8027 / +233 50 622 9589",
    "END:VEVENT", "END:VCALENDAR",
  ].join("\r\n");
  cal.href = "data:text/calendar;charset=utf-8," + encodeURIComponent(ics);
}

// ---------- Gallery lightbox ----------
const lb = $("#lightbox");
if (lb) {
  const items = $$("[data-lightbox]");
  const img = $("img", lb);
  const cap = $("figcaption", lb);
  let i = 0;
  let lastFocus;
  const show = (n) => {
    i = (n + items.length) % items.length;
    img.src = items[i].href;
    img.alt = $("img", items[i]).alt;
    cap.textContent = img.alt;
  };
  const close = () => { lb.hidden = true; document.body.style.overflow = ""; lastFocus && lastFocus.focus(); };
  items.forEach((a, n) => a.addEventListener("click", (e) => {
    e.preventDefault();
    lastFocus = a;
    show(n);
    lb.hidden = false;
    document.body.style.overflow = "hidden";
    $(".lb-close", lb).focus();
  }));
  $(".lb-close", lb).addEventListener("click", close);
  $(".lb-prev", lb).addEventListener("click", () => show(i - 1));
  $(".lb-next", lb).addEventListener("click", () => show(i + 1));
  lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
  document.addEventListener("keydown", (e) => {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") show(i - 1);
    if (e.key === "ArrowRight") show(i + 1);
  });
  // Swipe on phones
  let x0 = null;
  lb.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });
}

$("#year").textContent = new Date().getFullYear();
