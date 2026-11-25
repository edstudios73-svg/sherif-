const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

// ---------- Mobile menu ----------
const toggle = $(".menu-toggle");
const setNav = (open) => {
  document.body.classList.toggle("nav-open", open);
  toggle.setAttribute("aria-expanded", String(open));
  toggle.textContent = open ? "Close" : "Menu";
};
toggle.addEventListener("click", () => setNav(!document.body.classList.contains("nav-open")));
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setNav(false); });
matchMedia("(min-width: 961px)").addEventListener("change", (e) => { if (e.matches) setNav(false); });

// ---------- Mark today's meeting (Ghana is on UTC) ----------
const today = new Date().getUTCDay();
$$(`.times li[data-day="${today}"], .times-table tr[data-day="${today}"]`).forEach((el) => el.classList.add("is-today"));

// ---------- Event: time until it starts ----------
$$("[data-start]").forEach((ev) => {
  const out = $("[data-countdown]", ev);
  const start = new Date(ev.dataset.start);
  const end = new Date(ev.dataset.end);
  const update = () => {
    const now = new Date();
    if (now >= end) { out.textContent = "Took place"; return; }
    if (now >= start) { out.textContent = "Happening now"; return; }
    const days = Math.floor((start - now) / 86400000);
    out.textContent = days === 0 ? "Tonight" : days === 1 ? "Tomorrow" : `In ${days} days`;
  };
  update();
  setInterval(update, 60000);

  // Add to calendar (.ics)
  const ics = $("[data-ics]", ev);
  if (ics) {
    const fmt = (d) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
    const body = [
      "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//FDMI//Events//EN",
      "BEGIN:VEVENT", "UID:at-his-feet-2026@fdmi",
      `DTSTAMP:${fmt(new Date())}`, `DTSTART:${fmt(start)}`, `DTEND:${fmt(end)}`,
      "SUMMARY:At His Feet: worship all night (FDMI)",
      "LOCATION:Church premises\\, last stop Adjen-Kotoku\\, next to Pick N Nikki School\\, Accra",
      "DESCRIPTION:Call 059 660 9093 or 020 171 3589",
      "END:VEVENT", "END:VCALENDAR",
    ].join("\r\n");
    ics.href = "data:text/calendar;charset=utf-8," + encodeURIComponent(body);
  }
});

// ---------- Lightbox ----------
const lb = $("#lightbox");
if (lb) {
  const links = $$("[data-lightbox]");
  const img = $("img", lb);
  const cap = $("figcaption", lb);
  let i = 0;
  let opener = null;
  const show = (n) => {
    i = (n + links.length) % links.length;
    const thumb = $("img", links[i]);
    img.src = links[i].href;
    img.alt = thumb.alt;
    cap.textContent = thumb.alt;
  };
  const close = () => {
    lb.hidden = true;
    document.body.style.overflow = "";
    if (opener) opener.focus();
  };
  links.forEach((a, n) => a.addEventListener("click", (e) => {
    e.preventDefault();
    opener = a;
    show(n);
    lb.hidden = false;
    document.body.style.overflow = "hidden";
    $(".lb-close", lb).focus();
  }));
  const single = links.length < 2;
  $(".lb-prev", lb).hidden = single;
  $(".lb-next", lb).hidden = single;
  $(".lb-close", lb).addEventListener("click", close);
  $(".lb-prev", lb).addEventListener("click", () => show(i - 1));
  $(".lb-next", lb).addEventListener("click", () => show(i + 1));
  lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
  document.addEventListener("keydown", (e) => {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft" && !single) show(i - 1);
    if (e.key === "ArrowRight" && !single) show(i + 1);
  });
  let x0 = null;
  lb.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    if (x0 === null || single) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });
}

$$("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });
