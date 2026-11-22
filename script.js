// At His Feet: Friday 4 December 2026, 8:00 PM Ghana time (GMT, UTC+0).
const EVENT_START = new Date("2026-12-04T20:00:00Z");
const EVENT_END = new Date("2026-12-05T05:00:00Z"); // all night, estimated close

const countdown = document.getElementById("countdown");
const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;

function tick() {
  const now = new Date();
  if (now >= EVENT_END) {
    countdown.textContent = "Thank you to everyone who worshipped with us.";
    return false;
  }
  if (now >= EVENT_START) {
    countdown.textContent = "Happening now. Come and worship with us.";
    return true;
  }
  const s = Math.floor((EVENT_START - now) / 1000);
  const d = Math.floor(s / 86400), h = Math.floor((s % 86400) / 3600), m = Math.floor((s % 3600) / 60);
  countdown.textContent = `${plural(d, "day")}, ${plural(h, "hour")}, ${plural(m, "minute")} to go`;
  return true;
}
if (tick()) setInterval(tick, 30000);

// Add-to-calendar (.ics)
const fmt = (d) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
const ics = [
  "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//FDMI//At His Feet//EN",
  "BEGIN:VEVENT", "UID:at-his-feet-2026@fdmi",
  `DTSTAMP:${fmt(new Date())}`, `DTSTART:${fmt(EVENT_START)}`, `DTEND:${fmt(EVENT_END)}`,
  "SUMMARY:At His Feet: Worship All Night (FDMI)",
  "LOCATION:Church premises\\, last stop Adjen-Kotoku\\, next to Pick N Nikki School\\, Accra",
  "DESCRIPTION:Info: +233 59 470 8027 / +233 50 622 9589",
  "END:VEVENT", "END:VCALENDAR",
].join("\r\n");
document.getElementById("add-calendar").href = "data:text/calendar;charset=utf-8," + encodeURIComponent(ics);

document.getElementById("year").textContent = new Date().getFullYear();
