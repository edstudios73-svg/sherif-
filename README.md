# Sherrif's Special Waakye

A simple website for ordering food and booking catering from Sherrif's in Anyinam Zongo, near the Islamic JHS.

- `index.html`: home page with a hero whose food photos change every 5 seconds.
- `menu.html`: the three dishes (Hot & Spicy Waakye, Jollof Rice, Plain Rice). Customers tap + / −, choose delivery or pick-up, and the order opens in WhatsApp, ready to send to 053 581 5707.
- `book.html`: catering bookings for events, parties, weddings and funerals, sent the same way.

It's built for phones first, with a bottom tab bar on small screens and a top menu on desktop.

Icons are line icons from Lucide in `icons.svg`.

It's plain HTML, CSS and JavaScript with no build step. Open `index.html` in a browser, or host the folder on any static host (GitHub Pages, Netlify, Vercel).

To change the WhatsApp number, edit `WHATSAPP_NUMBER` in `script.js`. To change the food photos, replace the files in `images/`.
