// At His Feet: Friday 4 December 2026, 8:00 PM Ghana time (GMT, UTC+0).
const EVENT_START = new Date("2026-12-04T20:00:00Z");
const EVENT_END = new Date("2026-12-05T05:00:00Z"); // all night, estimated close

// Mobile menu
const toggle = document.querySelector(".menu-toggle");
const nav = document.getElementById("nav");
toggle.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(open));
  toggle.textContent = open ? "Close" : "Menu";
});
nav.addEventListener("click", (e) => {
  if (e.target.closest("a") && nav.classList.contains("open")) toggle.click();
});

// Countdown
const countdown = document.getElementById("countdown");
const done = document.getElementById("countdown-done");
const cells = Object.fromEntries(
  [...countdown.querySelectorAll("[data-unit]")].map((el) => [el.dataset.unit, el])
);
const pad = (n) => String(n).padStart(2, "0");

function tick() {
  const now = new Date();
  if (now >= EVENT_END) {
    countdown.hidden = true;
    done.hidden = false;
    return false;
  }
  const ms = Math.max(0, EVENT_START - now);
  const s = Math.floor(ms / 1000);
  cells.days.textContent = Math.floor(s / 86400);
  cells.hours.textContent = pad(Math.floor((s % 86400) / 3600));
  cells.minutes.textContent = pad(Math.floor((s % 3600) / 60));
  cells.seconds.textContent = pad(s % 60);
  return true;
}
// Only announce to screen readers once, not every second.
if (tick()) {
  countdown.setAttribute("aria-live", "off");
  setInterval(tick, 1000);
}

// Add-to-calendar (.ics) download
const fmt = (d) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
const ics = [
  "BEGIN:VCALENDAR",
  "VERSION:2.0",
  "PRODID:-//FDMI//At His Feet//EN",
  "BEGIN:VEVENT",
  "UID:at-his-feet-2026@fdmi",
  `DTSTAMP:${fmt(new Date())}`,
  `DTSTART:${fmt(EVENT_START)}`,
  `DTEND:${fmt(EVENT_END)}`,
  "SUMMARY:At His Feet: Worship All Night (FDMI)",
  "LOCATION:Church premises\\, last stop Adjen-Kotoku\\, next to Pick N Nikki School\\, Accra",
  "DESCRIPTION:All-night worship with Faith Demonstration Ministries International. Info: +233 59 470 8027 / +233 50 622 9589",
  "END:VEVENT",
  "END:VCALENDAR",
].join("\r\n");
document.getElementById("add-calendar").href =
  "data:text/calendar;charset=utf-8," + encodeURIComponent(ics);

document.getElementById("year").textContent = new Date().getFullYear();
