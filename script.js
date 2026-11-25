// ---------- Mobile menu ----------
const menuBtn = document.querySelector(".menu-btn");
const nav = document.getElementById("nav");
function setMenu(open) {
  nav.classList.toggle("open", open);
  menuBtn.setAttribute("aria-expanded", String(open));
  menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
}
menuBtn.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
nav.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

// ---------- Highlight current section in the nav ----------
const links = [...nav.querySelectorAll('a[href^="#"]')];
const sections = links.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id));
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  sections.forEach((s) => io.observe(s));
}

// ---------- Service times: highlight today (Ghana time = UTC) ----------
const today = new Date().getUTCDay();
const row = document.querySelector(`.times-row[data-day="${today}"]`);
const note = document.getElementById("today-note");
if (row) {
  row.classList.add("is-today");
  note.textContent = `There's a meeting today: ${row.querySelector(".t-name").textContent}, ${row.querySelector(".t-time").textContent}. We'd love to see you.`;
} else {
  const next = [...document.querySelectorAll(".times-row[data-day]")]
    .map((r) => ({ r, d: (Number(r.dataset.day) - today + 7) % 7 }))
    .sort((a, b) => a.d - b.d)[0];
  note.textContent = `Next meeting: ${next.r.querySelector(".t-day").textContent}, ${next.r.querySelector(".t-name").textContent} at ${next.r.querySelector(".t-time").textContent}.`;
}
note.hidden = false;

// ---------- At His Feet countdown ----------
// Friday 4 December 2026, 8:00 PM Ghana time (GMT, UTC+0). All night.
const START = new Date("2026-12-04T20:00:00Z");
const END = new Date("2026-12-05T05:00:00Z");
const cd = document.getElementById("countdown");
const cdMsg = document.getElementById("countdown-msg");
const cells = Object.fromEntries([...cd.querySelectorAll("[data-u]")].map((el) => [el.dataset.u, el]));
const pad = (n) => String(n).padStart(2, "0");
let timer;
function tick() {
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
}
tick();
timer = setInterval(tick, 1000);

// ---------- Add to calendar (.ics) ----------
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
document.getElementById("add-calendar").href = "data:text/calendar;charset=utf-8," + encodeURIComponent(ics);

document.getElementById("year").textContent = new Date().getFullYear();
