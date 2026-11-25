#!/usr/bin/env python3
"""Builds the static pages of the FDMI website.

Every page shares one header, footer and phone tab bar, defined here once.
Edit the content below, then run:  python3 build.py
"""
from pathlib import Path

SITE = "https://fdmi-church.vercel.app"
WA = "https://wa.me/233596609093"
OG = f"{SITE}/assets/og-card.jpg"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("leaders.html", "Leaders"),
    ("gallery.html", "Gallery"),
    ("events.html", "Events"),
    ("visit.html", "Visit"),
]

# ---------------------------------------------------------------- shared bits
ICON = {
    "home": '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "photo": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 17l-5-5-9 8"/>',
    "wa": '<path d="M3 21l1.7-5A8.5 8.5 0 1 1 8 19.3z"/>',
    "pin": '<path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "fb": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8z"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>',
    "tt": '<path d="M14 3v11a4 4 0 1 1-4-4"/><path d="M14 3c0 3 2 5 5 5"/>',
    "yt": '<rect x="2" y="5" width="20" height="14" rx="4"/><path d="M10 9l5 3-5 3z" fill="currentColor"/>',
    "play": '<path d="M8 5l11 7-11 7z" fill="currentColor"/>',
}


def svg(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg>'


SERVICES = [  # (weekday 0=Sun, day, meeting, time)
    (0, "Sunday", "Divine Service", "8:30 – 11:00 AM"),
    (2, "Tuesday", "Study His Word", "6:00 – 8:30 PM"),
    (3, "Wednesday", "Grace Hour", "9:00 AM – 12:00 noon"),
    (5, "Friday", "Liberation and Prophetic Hour", "6:30 – 9:00 PM"),
]


def times_table():
    rows = "\n".join(
        f'''          <div class="times-row" role="row" data-day="{d}">
            <span role="cell" class="t-day">{day}</span><span role="cell" class="t-name">{name}</span><span role="cell" class="t-time">{t}</span>
          </div>''' for d, day, name, t in SERVICES)
    return f'''<div class="times" role="table" aria-label="Weekly service times">
          <div class="times-row times-headrow" role="row">
            <span role="columnheader">Day</span><span role="columnheader">Meeting</span><span role="columnheader">Time</span>
          </div>
{rows}
        </div>
        <p class="today-note" id="today-note" hidden></p>'''


def header(active):
    links = "\n".join(
        f'        <a href="{href}"{" class=\"active\" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV)
    return f'''  <a class="skip" href="#main">Skip to content</a>
  <header class="bar" id="top">
    <div class="bar-inner">
      <a class="brand" href="index.html">
        <img src="assets/fdmi-crest.jpg" alt="" width="40" height="40">
        <span class="brand-text"><strong>Faith Demonstration</strong><small>Ministries International</small></span>
      </a>
      <nav class="nav" id="nav" aria-label="Main">
{links}
      </nav>
      <a class="pill pill-gold bar-cta" href="{WA}">WhatsApp us</a>
      <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </header>'''


def footer():
    starts = ["8:30 AM", "6:00 PM", "9:00 AM", "6:30 PM"]
    foot_times = "\n".join(
        f'          <li><span>{day} {name.replace(" and Prophetic", "")}</span><b>{st}</b></li>'
        for (_, day, name, _t), st in zip(SERVICES, starts))
    nav = "\n".join(f'          <li><a href="{h}">{l}</a></li>' for h, l in NAV[1:])
    return f'''  <footer class="foot">
    <div class="wrap foot-grid">
      <div class="foot-brand">
        <a class="brand" href="index.html">
          <img src="assets/fdmi-crest.jpg" alt="" width="48" height="48">
          <span class="brand-text"><strong>Faith Demonstration</strong><small>Ministries International</small></span>
        </a>
        <p>Last stop, Adjen-Kotoku, next to Pick N Nikki School, Accra, Ghana.</p>
        <p class="foot-phones"><a href="tel:+233596609093">059 660 9093</a> &middot; <a href="tel:+233201713589">020 171 3589</a></p>
        <ul class="socials">
          <li><a href="https://www.facebook.com/search/top?q=FAITH%20Demonstration%20Ministries%20International" aria-label="Facebook">{svg("fb")}</a></li>
          <li><a href="https://www.instagram.com/apostlevictorannan" aria-label="Instagram">{svg("ig")}</a></li>
          <li><a href="https://www.tiktok.com/@apostlevictorannan" aria-label="TikTok">{svg("tt")}</a></li>
          <li><a href="https://www.youtube.com/results?search_query=faith+demonstration+ministries+victor+annan" aria-label="YouTube">{svg("yt")}</a></li>
          <li><a href="{WA}" aria-label="WhatsApp">{svg("wa")}</a></li>
        </ul>
      </div>
      <div>
        <h4>Explore</h4>
        <ul class="foot-links">
{nav}
        </ul>
      </div>
      <div>
        <h4>Service times</h4>
        <ul class="foot-times">
{foot_times}
        </ul>
      </div>
    </div>
    <p class="wrap foot-legal">&copy; <span id="year">2026</span> Faith Demonstration Ministries International, Adjen-Kotoku, Accra.</p>
  </footer>

  <nav class="tabbar" aria-label="Quick actions">
    <a href="index.html">{svg("home")}<span>Home</span></a>
    <a href="visit.html#times">{svg("clock")}<span>Times</span></a>
    <a href="events.html">{svg("cal")}<span>Events</span></a>
    <a href="gallery.html">{svg("photo")}<span>Gallery</span></a>
    <a href="{WA}" class="tab-gold">{svg("wa")}<span>WhatsApp</span></a>
  </nav>'''


def page(file, title, desc, body, og_title=None):
    full_title = title if file == "index.html" else f"{title} | Faith Demonstration Ministries International"
    url = SITE + "/" + ("" if file == "index.html" else file)
    return f'''<!DOCTYPE html>
<html lang="en-GH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#5e1420">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Faith Demonstration Ministries International">
  <meta property="og:locale" content="en_GH">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{og_title or full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{OG}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Faith Demonstration Ministries International, Adjen-Kotoku, Accra">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title or full_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{OG}">
  <link rel="icon" href="assets/fdmi-crest.jpg">
  <link rel="apple-touch-icon" href="assets/fdmi-crest.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,500&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
{header(file)}

  <main id="main">
{body}
  </main>

{footer()}

  <script src="script.js"></script>
</body>
</html>
'''


def page_hero(img, eyebrow, title, text, pos="50% 40%"):
    return f'''    <section class="page-hero">
      <img class="page-hero-img" src="{img}" alt="" style="object-position:{pos}">
      <div class="page-hero-shade" aria-hidden="true"></div>
      <div class="wrap page-hero-body">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p>{text}</p>
      </div>
    </section>'''


def photo_card(img, title, text, href=None, pos="50% 40%"):
    inner = f'''<img src="{img}" alt="" loading="lazy" style="object-position:{pos}">
            <div class="photo-card-body"><h3>{title}</h3><p>{text}</p></div>'''
    if href:
        return f'          <a class="photo-card" href="{href}">{inner}</a>'
    return f'          <article class="photo-card">{inner}</article>'


VERSE = '''        <figure class="verse">
          <p class="eyebrow">Why we're called Faith Demonstration</p>
          <blockquote>My message and my preaching were not with wise and persuasive words, but with a demonstration of the Spirit's power, so that your faith might not rest on human wisdom, but on God's power.</blockquote>
          <figcaption>1 Corinthians 2:4–5</figcaption>
        </figure>'''

PRAYER_BTN = f'''        <div class="center">
          <a class="pill pill-wine pill-lg" href="{WA}?text=Hello%2C%20I%20would%20like%20to%20send%20a%20prayer%20request.">Send a prayer request</a>
        </div>'''

EVENT_CARD = f'''        <article class="event">
          <a class="event-flyer" href="assets/at-his-feet-flyer.jpg">
            <img src="assets/at-his-feet-flyer.jpg" alt="At His Feet worship all night flyer, Friday 4th December 2026, 8:00 PM" width="720" height="1007" loading="lazy">
          </a>
          <div class="event-body">
            <p class="eyebrow eyebrow-left">Save the date</p>
            <h2>At His Feet</h2>
            <p class="event-sub">Worship all night</p>
            <ul class="event-facts">
              <li><strong>Friday 4 December 2026</strong>, from 8:00 PM</li>
              <li>Church premises, last stop Adjen-Kotoku, next to Pick N Nikki School</li>
              <li>With Bishop Victor Annan, Rev. Mrs Natalie Annan, Rose Adjei, Anita Binney, Pastor Albert Abekah, Lady Rev. Nana Serwaa Yeboah, Nana Ama and Abore Junior</li>
            </ul>
            <div class="countdown" id="countdown" aria-label="Time until At His Feet">
              <div><b data-u="d">--</b><span>days</span></div>
              <div><b data-u="h">--</b><span>hours</span></div>
              <div><b data-u="m">--</b><span>mins</span></div>
              <div><b data-u="s">--</b><span>secs</span></div>
            </div>
            <p class="countdown-msg" id="countdown-msg" hidden></p>
            <div class="event-actions">
              <a class="pill pill-wine" id="add-calendar" href="#" download="at-his-feet.ics">Add to calendar</a>
              <a class="pill pill-line" href="tel:+233596609093">Call for info</a>
            </div>
          </div>
        </article>'''

MAP = '''<div class="find-map">
            <iframe title="Map showing Adjen-Kotoku, Accra" src="https://maps.google.com/maps?q=Adjen%20Kotoku%2C%20Accra%2C%20Ghana&amp;z=14&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          </div>'''

FIND_DETAILS = '''<dl>
              <div><dt>Address</dt><dd>Last stop, Adjen-Kotoku (Medie-Kotoku area), Accra, Ghana</dd></div>
              <div><dt>Landmark</dt><dd>Next to Pick N Nikki School</dd></div>
              <div><dt>Phone</dt><dd><a href="tel:+233596609093">059 660 9093</a></dd></div>
              <div><dt>Phone</dt><dd><a href="tel:+233201713589">020 171 3589</a></dd></div>
              <div><dt>WhatsApp</dt><dd><a href="https://wa.me/233596609093">059 660 9093</a></dd></div>
            </dl>'''

DIRECTIONS = "https://www.google.com/maps/search/?api=1&amp;query=Pick+N+Nikki+School+Adjen+Kotoku+Accra"

LEADER_APOSTLE = '''          <article class="leader">
            <img src="assets/victor-annan.jpg" alt="Apostle Victor Annan" width="440" height="440" loading="lazy">
            <div class="leader-body">
              <p class="eyebrow eyebrow-left">Head of the ministry</p>
              <h3>Apostle Victor Annan</h3>
              <p>A minister of the Gospel of our Lord Jesus Christ, Apostle Annan leads the ministry with a deep prophetic and apostolic grace, and a heart to see faith demonstrated in everyday lives.</p>
            </div>
          </article>'''

LEADER_NATALIE = '''          <article class="leader">
            <img src="assets/natalie-annan.jpg" alt="Rev. Mrs Natalie Annan" width="440" height="440" loading="lazy">
            <div class="leader-body">
              <p class="eyebrow eyebrow-left">Ministering alongside the Apostle</p>
              <h3>Rev. Mrs Natalie Annan</h3>
              <p>Rev. Mrs Annan serves alongside the Apostle, caring for the church family and ministering in worship and the Word.</p>
            </div>
          </article>'''

GALLERY = [  # (file, caption, wide?)
    ("white-service-2", "A night of prayer at FDMI", True),
    ("church-family", "The FDMI family together", True),
    ("consecration", "Laying on of hands", False),
    ("youth", "Our young people", True),
    ("child-dedication", "Child dedication", False),
    ("congregation-joy", "Joy in the house", True),
    ("women-celebration", "Celebrating together", False),
    ("white-service-1", "In white, before the Lord", True),
    ("blessing", "A word of blessing", False),
    ("night-prayer", "Night of prayer", False),
    ("clergy-vestments", "Shepherds of the house", False),
    ("white-service-3", "Standing together in prayer", True),
    ("worship-team", "Leading the house in worship", True),
    ("youth-night", "Youth night", True),
    ("family-celebration", "Family celebration", True),
    ("white-service-4", "Prayer under the FDMI letters", True),
]


def gallery_item(f, cap, wide):
    return (f'          <figure class="g-item{" g-wide" if wide else ""}"><a href="assets/photos/{f}.jpg" data-lightbox>'
            f'<img src="assets/photos/{f}.jpg" alt="{cap}" loading="lazy"></a><figcaption>{cap}</figcaption></figure>')


VIDEO = f'''<figure class="video-card">
            <video controls preload="none" playsinline poster="assets/video/children-celebration.jpg">
              <source src="assets/video/children-celebration.mp4" type="video/mp4">
            </video>
            <figcaption>Our children dancing for joy at a church celebration</figcaption>
          </figure>'''

TEAM_MEMBERS = [  # (photo, position, name) - add names when confirmed
    ("assets/people/church-elder.jpg", "Church Elder", ""),
    ("assets/people/church-secretary.jpg", "Church Secretary", ""),
]
TEAM = "\n".join(
    f'''          <article class="member">
            <img src="{img}" alt="{name or 'FDMI ' + role}" width="440" height="440" loading="lazy">
            <h3>{name or role}</h3>
            {f'<p>{role}</p>' if name else ''}
          </article>''' for img, role, name in TEAM_MEMBERS)

# ---------------------------------------------------------------- pages
pages = {}

pages["index.html"] = page("index.html",
    "Faith Demonstration Ministries International | Adjen-Kotoku, Accra",
    "A prophetic and apostolic church at Adjen-Kotoku, Accra, led by Apostle Victor Annan. Sunday Divine Service 8:30 AM. Everybody is welcome.",
    f'''    <section class="hero">
      <img class="hero-img" src="assets/photos/white-service-2.jpg" alt="Worship at FDMI, with the gold F D M I letters on the wall" width="1280" height="960">
      <div class="hero-shade" aria-hidden="true"></div>
      <div class="hero-body wrap">
        <p class="eyebrow">You are welcome</p>
        <h1>Faith Demonstration <span>Ministries International</span></h1>
        <p class="hero-tag">A prophetic and apostolic church in Adjen-Kotoku, Accra</p>
        <p class="hero-copy">Led by Apostle Victor Annan, we gather to worship, study His Word and see the power of God at work. Our Divine Service is every Sunday from 8:30 AM. Come as you are.</p>
        <div class="hero-actions">
          <a class="pill pill-gold pill-lg" href="visit.html">Plan your visit</a>
          <a class="pill pill-glass pill-lg" href="#times">See service times</a>
        </div>
      </div>
    </section>

    <section class="section tint">
      <div class="wrap">
        <header class="head">
          <p class="eyebrow">What we're about</p>
          <h2>Faith that is shown, not only spoken</h2>
          <p>Everything we do comes from the Word of God and is led by the Holy Spirit.</p>
        </header>
        <div class="photo-cards">
{photo_card("assets/photos/worship-team.jpg", "Worship", "Spirit-filled praise every service.", "about.html")}
{photo_card("assets/photos/congregation-joy.jpg", "The Word", "Practical teaching at Study His Word.", "about.html", "50% 30%")}
{photo_card("assets/photos/blessing.jpg", "Prayer", "Grace Hour and the Liberation Hour.", "about.html", "50% 35%")}
{photo_card("assets/photos/child-dedication.jpg", "Family", "A home for every age.", "about.html", "50% 25%")}
        </div>
        <div class="center more"><a class="pill pill-line" href="about.html">More about us</a></div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <article class="feature">
          <img src="assets/photos/consecration.jpg" alt="Laying on of hands at FDMI" loading="lazy">
          <div class="feature-body">
            <p class="eyebrow eyebrow-left">Our leadership</p>
            <h2>Apostle Victor Annan</h2>
            <p>The ministry is led by Apostle Victor Annan, with Rev. Mrs Natalie Annan ministering alongside him. Together with our ministers and leaders, they shepherd the FDMI family in Adjen-Kotoku.</p>
            <a class="pill pill-wine" href="leaders.html">Meet our leaders</a>
          </div>
        </article>
      </div>
    </section>

    <section class="section tint" id="times">
      <div class="wrap wrap-narrow">
        <header class="head">
          <p class="eyebrow">Join us this week</p>
          <h2>Our service times</h2>
          <p>All meetings hold at the church premises, last stop Adjen-Kotoku, Accra.</p>
        </header>
        {times_table()}
        <a class="pill pill-wine pill-block" href="visit.html">Plan your visit</a>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
{EVENT_CARD}
        <div class="center more"><a class="pill pill-line" href="events.html">View all events</a></div>
      </div>
    </section>

    <section class="section tint">
      <div class="wrap">
        <header class="head">
          <p class="eyebrow">Life at FDMI</p>
          <h2>Moments from the house</h2>
        </header>
        <div class="strip">
{chr(10).join(gallery_item(f, c, False) for f, c, _ in [GALLERY[1], GALLERY[3], GALLERY[4], GALLERY[5], GALLERY[6], GALLERY[9]])}
        </div>
        <div class="center more"><a class="pill pill-wine" href="gallery.html">Open the gallery</a></div>
      </div>
    </section>

    <section class="section">
      <div class="wrap wrap-narrow">
        <header class="head">
          <p class="eyebrow">Find us</p>
          <h2>Where we are</h2>
        </header>
        <article class="find">
          {MAP}
          <div class="find-body">
            <h3>Find us in Adjen-Kotoku</h3>
            {FIND_DETAILS}
            <a class="pill pill-line pill-block" href="{DIRECTIONS}">Get directions on Google Maps</a>
          </div>
        </article>
      </div>
    </section>

    <section class="section tint">
      <div class="wrap wrap-narrow">
{VERSE}
{PRAYER_BTN}
      </div>
    </section>''',
    og_title="Faith Demonstration Ministries International | Adjen-Kotoku, Accra")

pages["about.html"] = page("about.html", "About us",
    "Faith Demonstration Ministries International is a prophetic and apostolic church in Adjen-Kotoku, Accra, led by Apostle Victor Annan.",
    f'''{page_hero("assets/photos/church-family.jpg", "About us", "A family of faith in Adjen-Kotoku", "Faith Demonstration Ministries International is a prophetic and apostolic church in Accra, Ghana, led by Apostle Victor Annan.", "50% 30%")}

    <section class="section">
      <div class="wrap split">
        <div class="split-text">
          <p class="eyebrow eyebrow-left">Who we are</p>
          <h2>Faith that is shown, not only spoken</h2>
          <p>We gather to worship, to hear the Word of God and to see it at work in everyday lives: in healing, in restoration and in families made whole.</p>
          <p>Our name comes from the Apostle Paul's words to the church in Corinth. He did not come with clever words, but with a demonstration of the Spirit's power, so that faith would rest on God and not on people.</p>
          <p>Whether you have walked with Jesus for years or you are only beginning to ask questions, there is a seat for you in the house.</p>
        </div>
        <img class="split-img" src="assets/photos/white-service-3.jpg" alt="Members dressed in white at a prayer service" loading="lazy">
      </div>
    </section>

    <section class="section tint">
      <div class="wrap">
        <header class="head">
          <p class="eyebrow">What we're about</p>
          <h2>Four things that shape us</h2>
        </header>
        <div class="photo-cards">
{photo_card("assets/photos/worship-team.jpg", "Worship", "Spirit-filled praise every service, and all-night worship on special nights.")}
{photo_card("assets/photos/congregation-joy.jpg", "The Word", "Practical Bible teaching every Tuesday at Study His Word.", pos="50% 30%")}
{photo_card("assets/photos/blessing.jpg", "Prayer", "Grace Hour on Wednesdays and the Liberation and Prophetic Hour on Fridays.", pos="50% 35%")}
{photo_card("assets/photos/child-dedication.jpg", "Family", "Children, young people and parents growing in faith together.", pos="50% 25%")}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split split-rev">
        <div class="split-text">
          <p class="eyebrow eyebrow-left">Children and youth</p>
          <h2>Room for the next generation</h2>
          <p>Our children and young people are at the heart of church life, in worship, in celebration and in service.</p>
          <a class="pill pill-wine" href="gallery.html">See more in the gallery</a>
        </div>
        {VIDEO}
      </div>
    </section>

    <section class="section tint">
      <div class="wrap wrap-narrow">
{VERSE}
{PRAYER_BTN}
      </div>
    </section>''')

pages["leaders.html"] = page("leaders.html", "Our leaders",
    "Meet the leadership of Faith Demonstration Ministries International: Apostle Victor Annan and Rev. Mrs Natalie Annan.",
    f'''{page_hero("assets/photos/consecration.jpg", "Our leadership", "Shepherds of the house", "The men and women God has given to lead and care for the FDMI family.", "50% 22%")}

    <section class="section">
      <div class="wrap">
        <div class="leaders">
{LEADER_APOSTLE}
{LEADER_NATALIE}
        </div>
      </div>
    </section>

    <section class="section tint">
      <div class="wrap">
        <header class="head">
          <p class="eyebrow">Ministry team</p>
          <h2>Serving the FDMI family</h2>
          <p>The leaders who help keep the house running, week by week.</p>
        </header>
        <div class="team">
{TEAM}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div class="split-text">
          <p class="eyebrow eyebrow-left">Called and consecrated</p>
          <h2>Set apart to serve</h2>
          <p>Our ministers are prayed over and set apart before the congregation, so that the whole church stands with them in the work God has given them.</p>
          <a class="pill pill-wine" href="gallery.html">See the gallery</a>
        </div>
        <img class="split-img split-img-tall" src="assets/photos/clergy-vestments.jpg" alt="Two ministers in clerical robes at FDMI" loading="lazy">
      </div>
    </section>''')

pages["gallery.html"] = page("gallery.html", "Gallery",
    "Photos and videos from worship, prayer, celebrations and church life at Faith Demonstration Ministries International, Accra.",
    f'''{page_hero("assets/photos/youth.jpg", "Gallery", "Life in the house", "Worship, prayer, celebrations and the FDMI family. Tap any photo to see it bigger.", "50% 30%")}

    <section class="section">
      <div class="wrap">
        <div class="gallery">
{chr(10).join(gallery_item(*g) for g in GALLERY)}
        </div>
      </div>
    </section>

    <section class="section tint">
      <div class="wrap wrap-narrow">
        <header class="head">
          <p class="eyebrow">Video</p>
          <h2>Children's celebration</h2>
        </header>
        {VIDEO}
      </div>
    </section>

    <div class="lightbox" id="lightbox" hidden>
      <button class="lb-close" aria-label="Close">&times;</button>
      <button class="lb-prev" aria-label="Previous photo">&#8249;</button>
      <figure><img alt=""><figcaption></figcaption></figure>
      <button class="lb-next" aria-label="Next photo">&#8250;</button>
    </div>''')

pages["events.html"] = page("events.html", "Events",
    "Upcoming events at Faith Demonstration Ministries International: At His Feet, worship all night on Friday 4 December 2026, plus our weekly meetings.",
    f'''{page_hero("assets/photos/night-prayer.jpg", "Events", "What's coming up", "Special services, all-night worship and our weekly meetings.", "50% 40%")}

    <section class="section">
      <div class="wrap">
{EVENT_CARD}
      </div>
    </section>

    <section class="section tint">
      <div class="wrap wrap-narrow">
        <header class="head">
          <p class="eyebrow">Every week</p>
          <h2>Our regular meetings</h2>
        </header>
        {times_table()}
        <a class="pill pill-wine pill-block" href="{WA}">Ask us about upcoming programmes</a>
      </div>
    </section>''')

pages["visit.html"] = page("visit.html", "Plan your visit",
    "Visit Faith Demonstration Ministries International at the last stop, Adjen-Kotoku, next to Pick N Nikki School, Accra. Service times, directions and contacts.",
    f'''{page_hero("assets/photos/women-celebration.jpg", "Plan your visit", "We'd love to welcome you", "Here's everything you need for your first Sunday with us.", "50% 20%")}

    <section class="section" id="times">
      <div class="wrap wrap-narrow">
        <header class="head">
          <p class="eyebrow">Join us this week</p>
          <h2>Service times</h2>
          <p>All meetings hold at the church premises, last stop Adjen-Kotoku, Accra.</p>
        </header>
        {times_table()}
      </div>
    </section>

    <section class="section tint">
      <div class="wrap">
        <header class="head">
          <p class="eyebrow">Your first visit</p>
          <h2>What to expect</h2>
        </header>
        <div class="expect">
          <article><h3>A warm welcome</h3><p>Our ushers will greet you at the door and help you find a seat.</p></article>
          <article><h3>Lively worship</h3><p>Expect heartfelt praise, prayer and the preaching of the Word.</p></article>
          <article><h3>Come as you are</h3><p>No special dress is needed. Wear what you're comfortable worshipping in.</p></article>
          <article><h3>Prayer for you</h3><p>If you need prayer, let an usher know or send us a message before you come.</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap wrap-narrow">
        <header class="head">
          <p class="eyebrow">Find us</p>
          <h2>Where we are</h2>
        </header>
        <article class="find">
          {MAP}
          <div class="find-body">
            <h3>Find us in Adjen-Kotoku</h3>
            {FIND_DETAILS}
            <div class="find-actions">
              <a class="pill pill-wine" href="{DIRECTIONS}">Get directions</a>
              <a class="pill pill-line" href="{WA}">WhatsApp us</a>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section class="section tint">
      <div class="wrap wrap-narrow">
{VERSE}
{PRAYER_BTN}
      </div>
    </section>''')

out = Path(__file__).parent
for name, html in pages.items():
    (out / name).write_text(html)
    print("wrote", name)
