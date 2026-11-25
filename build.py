#!/usr/bin/env python3
"""Builds the static pages of the FDMI website.

All pages share one header and footer, defined here once.
Edit the content below, then run:  python3 build.py
Don't edit the generated .html files by hand.
"""
from pathlib import Path
from urllib.parse import quote

SITE = "https://fdmi-church.vercel.app"
OG = f"{SITE}/assets/og-card.jpg"
WA_NUM = "233596609093"
WA = f"https://wa.me/{WA_NUM}"
PHONES = [("059 660 9093", "+233596609093"), ("020 171 3589", "+233201713589")]
ADDRESS = "Last stop, Adjen-Kotoku, next to Pick N Nikki School, Accra"
DIRECTIONS = "https://www.google.com/maps/search/?api=1&amp;query=Pick+N+Nikki+School+Adjen+Kotoku+Accra"
SOCIAL = [
    ("YouTube", "https://www.youtube.com/results?search_query=faith+demonstration+ministries+victor+annan"),
    ("Facebook", "https://www.facebook.com/search/top?q=FAITH%20Demonstration%20Ministries%20International"),
    ("Instagram", "https://www.instagram.com/apostlevictorannan"),
    ("TikTok", "https://www.tiktok.com/@apostlevictorannan"),
]

NAV = [
    ("about.html", "About"),
    ("leaders.html", "Leaders"),
    ("ministries.html", "Ministries"),
    ("sermons.html", "Sermons"),
    ("events.html", "Events"),
    ("announcements.html", "Announcements"),
]

SERVICES = [  # (weekday 0=Sun, day, meeting, time)
    (0, "Sunday", "Divine Service", "8:30 – 11:00 AM"),
    (2, "Tuesday", "Study His Word", "6:00 – 8:30 PM"),
    (3, "Wednesday", "Grace Hour", "9:00 AM – 12:00 noon"),
    (5, "Friday", "Liberation and Prophetic Hour", "6:30 – 9:00 PM"),
]


def wa(text):
    return f"{WA}?text={quote(text)}"


def phones_html(sep=" or "):
    return sep.join(f'<a href="tel:{t}">{n}</a>' for n, t in PHONES)


# ---------------------------------------------------------------- layout
def header(active):
    links = "\n".join(
        f'        <li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{l}</a></li>' for h, l in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="index.html" aria-label="Faith Demonstration Ministries International, home">
      <img src="assets/fdmi-crest.jpg" alt="" width="40" height="40">
      <span>Faith Demonstration<br>Ministries International</span>
    </a>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
{links}
      </ul>
      <a class="btn btn-dark nav-visit" href="visit.html">Plan a visit</a>
    </nav>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
  </div>
</header>'''


def footer():
    times = "\n".join(
        f'        <li><span>{d}</span><span>{m}<br><small>{t}</small></span></li>' for _, d, m, t in SERVICES)
    pages = "\n".join(f'        <li><a href="{h}">{l}</a></li>'
                      for h, l in NAV + [("visit.html", "Plan a visit"), ("gallery.html", "Gallery")])
    social = "\n".join(f'        <li><a href="{u}">{n}</a></li>' for n, u in SOCIAL + [("WhatsApp", WA)])
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-about">
      <img src="assets/fdmi-crest.jpg" alt="" width="56" height="56">
      <p class="footer-name">Faith Demonstration Ministries International</p>
      <p>{ADDRESS}</p>
      <p>{phones_html("<br>")}</p>
    </div>
    <div>
      <h2 class="footer-h">Services</h2>
      <ul class="footer-times">
{times}
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Pages</h2>
      <ul class="footer-list">
{pages}
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Follow</h2>
      <ul class="footer-list">
{social}
      </ul>
    </div>
  </div>
  <div class="container footer-base">
    <p>&copy; <span data-year>2026</span> Faith Demonstration Ministries International</p>
    <p>Adjen-Kotoku, Accra, Ghana</p>
  </div>
</footer>'''


def page(file, title, desc, body):
    full = ("Faith Demonstration Ministries International | Adjen-Kotoku, Accra" if file == "index.html"
            else f"{title} | Faith Demonstration Ministries International")
    url = SITE + "/" + ("" if file == "index.html" else file)
    return f'''<!DOCTYPE html>
<html lang="en-GH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1d1915">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Faith Demonstration Ministries International">
<meta property="og:locale" content="en_GH">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Faith Demonstration Ministries International, Adjen-Kotoku, Accra">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG}">
<link rel="icon" href="assets/fdmi-crest.jpg">
<link rel="apple-touch-icon" href="assets/fdmi-crest.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Schibsted+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body class="page-{file.replace('.html', '')}">
{header(file)}
<main id="main">
{body}
</main>
{footer()}
<script src="script.js"></script>
</body>
</html>
'''


def page_head(title, intro):
    return f'''<section class="page-head">
  <div class="container page-head-grid">
    <h1>{title}</h1>
    <p class="page-head-intro">{intro}</p>
  </div>
</section>'''


def times_list(cls=""):
    rows = "\n".join(
        f'    <li data-day="{n}"><span class="t-day">{d}</span><span class="t-name">{m}</span><span class="t-time">{t}</span></li>'
        for n, d, m, t in SERVICES)
    return f'''<ul class="times {cls}">
{rows}
  </ul>'''


# ---------------------------------------------------------------- content
EVENT = {
    "title": "At His Feet",
    "kind": "Worship all night",
    "date": "Friday 4 December 2026",
    "time": "From 8:00 PM",
    "start": "2026-12-04T20:00:00Z",
    "end": "2026-12-05T05:00:00Z",
    "place": "Church premises, last stop Adjen-Kotoku, next to Pick N Nikki School",
    "with": "Bishop Victor Annan, Rev. Mrs Natalie Annan, Rose Adjei, Anita Binney, Pastor Albert Abekah, Lady Rev. Nana Serwaa Yeboah, Nana Ama and Abore Junior",
}

ANNOUNCEMENTS = [  # (date label, title, body html, (link, label) or None)
    ("4 Dec 2026", "At His Feet: worship all night",
     "Join us on Friday 4 December from 8:00 PM for a night of worship with Bishop Victor Annan, Rev. Mrs Natalie Annan, Rose Adjei, Anita Binney and other ministers. Everyone is welcome.",
     ("events.html", "Event details")),
    ("Ongoing", "Church building project",
     f"We are raising support to build a permanent home for the church. To give towards the church project, speak to the Church Secretary after service or call {phones_html()}.",
     None),
    ("Ongoing", "Send your prayer requests",
     "You can send a prayer request at any time on WhatsApp. Our ministers pray over every request.",
     (wa("Hello, I would like to send a prayer request."), "Send a prayer request")),
    ("Updated", "Church phone numbers",
     f"You can reach the church on {phones_html()}. WhatsApp messages go to 059 660 9093.",
     None),
]

MINISTRIES = [  # (id, name, photo, object-position, text, WhatsApp message)
    ("worship", "Worship", "assets/photos/worship-team.jpg", "50% 45%",
     "The worship team leads the house in praise at every service, and through the night at all-night worship services like At His Feet.",
     "Hello, I would like to join the worship team."),
    ("prayer", "Prayer", "assets/photos/white-service-4.jpg", "50% 50%",
     "Prayer runs through the whole week. Grace Hour meets on Wednesday mornings and the Liberation and Prophetic Hour on Friday evenings.",
     "Hello, I would like to know more about the prayer ministry."),
    ("youth", "Youth", "assets/photos/youth-night.jpg", "50% 40%",
     "Young people meet, worship and grow together. In line with our focus, we want to train them with vocational skills for life.",
     "Hello, I would like to join the youth ministry."),
    ("children", "Children", "assets/photos/child-dedication.jpg", "50% 25%",
     "From dedication onwards, children are part of the church family. They are taught, prayed for and celebrated.",
     "Hello, I would like to know more about the children's ministry."),
    ("outreach", "Outreach and welfare", "assets/photos/church-family.jpg", "50% 35%",
     "Our goals are to reach the unreached, to help the less privileged and to help the aged. We serve the sub-communities around us.",
     "Hello, I would like to help with outreach and welfare."),
]

GALLERY = [  # (file in assets/photos, caption)
    ("white-service-2", "A night of prayer at FDMI"),
    ("church-family", "The FDMI family together"),
    ("consecration", "Laying on of hands"),
    ("worship-team", "Leading the house in worship"),
    ("youth", "Our young people"),
    ("child-dedication", "Child dedication"),
    ("congregation-joy", "Joy in the house"),
    ("women-celebration", "Celebrating together"),
    ("youth-night", "Youth night"),
    ("white-service-1", "In white, before the Lord"),
    ("blessing", "A word of blessing"),
    ("family-celebration", "Family celebration"),
    ("night-prayer", "Night of prayer"),
    ("clergy-vestments", "Shepherds of the house"),
    ("white-service-3", "Standing together in prayer"),
    ("white-service-4", "Prayer under the FDMI letters"),
]

TEAM = [  # (photo, position, name) - add names when confirmed
    ("assets/people/church-elder.jpg", "Church Elder", ""),
    ("assets/people/church-secretary.jpg", "Church Secretary", ""),
]


def event_feature(full=False):
    e = EVENT
    extra = f'''
        <p class="event-with"><span>Ministering</span> {e["with"]}</p>''' if full else ""
    actions = f'''
        <div class="actions">
          <a class="btn btn-dark" data-ics href="#" download="at-his-feet.ics">Add to calendar</a>
          <a class="btn btn-line" href="tel:{PHONES[0][1]}">Call {PHONES[0][0]}</a>
        </div>''' if full else '''
        <a class="text-link" href="events.html">Event details</a>'''
    return f'''<article class="event{' event-full' if full else ''}" data-start="{e["start"]}" data-end="{e["end"]}">
      <a class="event-flyer" href="assets/at-his-feet-flyer.jpg" data-lightbox>
        <img src="assets/at-his-feet-flyer.jpg" alt="At His Feet flyer: worship all night, Friday 4th December 2026, 8:00 PM" width="720" height="1007" loading="lazy">
      </a>
      <div class="event-body">
        <p class="event-date"><time datetime="2026-12-04">{e["date"]}</time><span data-countdown></span></p>
        <h3 class="event-title">{e["title"]}</h3>
        <p class="event-kind">{e["kind"]}</p>
        <dl class="event-meta">
          <div><dt>Time</dt><dd>{e["time"]}</dd></div>
          <div><dt>Place</dt><dd>{e["place"]}</dd></div>
        </dl>{extra}{actions}
      </div>
    </article>'''


def announcement(a, compact=False):
    date, title, body, link = a
    more = f'<a class="text-link" href="{link[0]}">{link[1]}</a>' if link else ""
    if compact:
        return f'''          <li class="notice">
            <p class="notice-date">{date}</p>
            <p class="notice-title">{title}</p>
          </li>'''
    return f'''    <article class="notice-full">
      <p class="notice-date">{date}</p>
      <div>
        <h2>{title}</h2>
        <p>{body}</p>
        {more}
      </div>
    </article>'''


def gallery_fig(f, cap):
    return (f'      <figure class="g-item"><a href="assets/photos/{f}.jpg" data-lightbox>'
            f'<img src="assets/photos/{f}.jpg" alt="{cap}" loading="lazy"></a><figcaption>{cap}</figcaption></figure>')


VIDEO = '''<figure class="video">
      <video controls preload="none" playsinline poster="assets/video/children-celebration.jpg">
        <source src="assets/video/children-celebration.mp4" type="video/mp4">
      </video>
    </figure>'''

LIGHTBOX = '''<div class="lightbox" id="lightbox" hidden>
  <button class="lb-close" type="button">Close</button>
  <button class="lb-prev" type="button" aria-label="Previous photo">&#8592;</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" type="button" aria-label="Next photo">&#8594;</button>
</div>'''

MAP = '''<div class="map">
    <iframe title="Map of Adjen-Kotoku, Accra" src="https://maps.google.com/maps?q=Adjen%20Kotoku%2C%20Accra%2C%20Ghana&amp;z=14&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>'''

# ---------------------------------------------------------------- pages
pages = {}

pages["index.html"] = page("index.html", "Home",
    "A prophetic and apostolic church at Adjen-Kotoku, Accra, led by Apostle Victor Annan. Sunday Divine Service from 8:30 AM. Everyone is welcome.",
    f'''<section class="hero">
  <img class="hero-img" src="assets/photos/white-service-2.jpg" alt="The congregation in prayer under the gold F D M I letters" width="1280" height="960">
  <div class="container hero-content">
    <h1>Faith Demonstration Ministries International</h1>
    <p>A prophetic and apostolic church at Adjen-Kotoku, Accra, led by Apostle Victor Annan.</p>
    <div class="actions">
      <a class="btn btn-gold" href="visit.html">Plan a visit</a>
      <a class="text-link text-link-light" href="#this-week">Service times</a>
    </div>
  </div>
</section>

<section class="week" id="this-week" aria-label="Weekly services">
  <div class="container">
  {times_list("times-band")}
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split-text">
      <h2>You're welcome here</h2>
      <p class="lead">We are a family of believers who gather to worship, to hear the undiluted Word of God and to see it at work in everyday lives.</p>
      <p>Our vision is to raise an indigenous and self-supporting church, and to demonstrate the love of God in our generation. Whether you have walked with Jesus for years or are only beginning to ask questions, there is a seat for you.</p>
      <a class="text-link" href="about.html">About the church</a>
    </div>
    <figure class="split-photo">
      <img src="assets/photos/worship-team.jpg" alt="The worship team singing on stage in front of the F D M I letters" loading="lazy">
    </figure>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    <div class="sec-head">
      <h2>Coming up</h2>
      <a class="text-link" href="events.html">All events</a>
    </div>
    <div class="upcoming">
    {event_feature()}
      <div class="notices-side">
        <h3 class="side-h">Announcements</h3>
        <ul class="notices">
{chr(10).join(announcement(a, compact=True) for a in ANNOUNCEMENTS[1:3])}
        </ul>
        <a class="text-link" href="announcements.html">All announcements</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head">
      <h2>Ministries</h2>
      <a class="text-link" href="ministries.html">All ministries</a>
    </div>
    <div class="tiles">
{chr(10).join(f'      <a class="tile" href="ministries.html#{m[0]}"><img src="{m[2]}" alt="" loading="lazy" style="object-position:{m[3]}"><span>{m[1]}</span></a>' for m in MINISTRIES[:4])}
    </div>
  </div>
</section>

<section class="feature-band">
  <img src="assets/photos/consecration.jpg" alt="Laying on of hands at FDMI" loading="lazy" style="object-position:50% 25%">
  <div class="feature-band-text">
    <h2>Led by Apostle Victor Annan</h2>
    <p>Apostle Victor Annan leads the ministry with a deep prophetic and apostolic grace, with Rev. Mrs Natalie Annan ministering alongside him.</p>
    <a class="text-link text-link-light" href="leaders.html">Meet our leaders</a>
  </div>
</section>

<section class="section">
  <div class="container split split-even">
    <div class="split-text">
      <h2>Missed a Sunday?</h2>
      <p>Catch up on messages from Divine Service and Study His Word on our pages.</p>
      <a class="text-link" href="sermons.html">Sermons</a>
    </div>
    <div class="split-text">
      <h2>Find us</h2>
      <p>{ADDRESS}.<br>Call {phones_html()}.</p>
      <a class="text-link" href="visit.html">Directions and what to expect</a>
    </div>
  </div>
</section>
{LIGHTBOX}''')

pages["about.html"] = page("about.html", "About the church",
    "Our vision is to raise an indigenous and self-supporting church and to demonstrate the love of God in our generation. Read FDMI's mission, focus and goals.",
    f'''{page_head("About the church", "Faith Demonstration Ministries International is a prophetic and apostolic church at Adjen-Kotoku, Accra, led by Apostle Victor Annan.")}

<div class="container">
  <figure class="wide-photo">
    <img src="assets/photos/church-family.jpg" alt="The FDMI family gathered in front of the church banner" loading="lazy">
  </figure>
</div>

<section class="section">
  <div class="container prose-grid">
    <h2>Our name</h2>
    <div class="prose">
      <p class="lead">Our name comes from the Apostle Paul's words to the church in Corinth.</p>
      <blockquote class="scripture">
        <p>My message and my preaching were not with wise and persuasive words, but with a demonstration of the Spirit's power, so that your faith might not rest on human wisdom, but on God's power.</p>
        <cite>1 Corinthians 2:4–5</cite>
      </blockquote>
      <p>We want faith that is seen as well as spoken: in worship, in healing and restoration, and in families made whole.</p>
    </div>
  </div>
</section>

<section class="vision">
  <div class="container prose-grid">
    <h2>Our vision</h2>
    <p class="vision-text">To raise an indigenous and self&#8209;supporting church, and to demonstrate the love of God in our generation.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="columns-3">
      <div class="col">
        <h2>Mission</h2>
        <ol class="plain-list">
          <li>To preach the undiluted Word of God.</li>
          <li>Spiritual growth, numerical growth and financial growth.</li>
          <li>Equipping the saints of Christ (Ephesians 4:11–13).</li>
        </ol>
      </div>
      <div class="col">
        <h2>Focus</h2>
        <p>Our focus is the sub-communities around us, the youth and the children, training them with vocational skills.</p>
      </div>
      <div class="col">
        <h2>Goals</h2>
        <ol class="plain-list">
          <li>To reach the unreached.</li>
          <li>To help the less privileged.</li>
          <li>To help the aged.</li>
        </ol>
      </div>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="container link-grid">
    <a href="leaders.html"><h2>Leaders</h2><p>Apostle Victor Annan, Rev. Mrs Natalie Annan and the ministry team.</p></a>
    <a href="ministries.html"><h2>Ministries</h2><p>Worship, prayer, youth, children, and outreach and welfare.</p></a>
    <a href="gallery.html"><h2>Gallery</h2><p>Photos and video from life in the church.</p></a>
  </div>
</section>''')

team_cards = "\n".join(
    f'''      <figure class="member">
        <img src="{img}" alt="{name or 'FDMI ' + role}" width="440" height="440" loading="lazy">
        <figcaption>{f"<strong>{name}</strong>{role}" if name else f"<strong>{role}</strong>"}</figcaption>
      </figure>''' for img, role, name in TEAM)

pages["leaders.html"] = page("leaders.html", "Leaders",
    "Meet the leadership of Faith Demonstration Ministries International: Apostle Victor Annan, Rev. Mrs Natalie Annan and the ministry team.",
    f'''{page_head("Leaders", "The men and women God has given to lead and care for the FDMI family.")}

<section class="section section-top-tight">
  <div class="container leaders">
    <article class="leader">
      <img src="assets/victor-annan.jpg" alt="Apostle Victor Annan" width="440" height="440" loading="lazy">
      <div class="leader-text">
        <p class="role">Head of the ministry</p>
        <h2>Apostle Victor Annan</h2>
        <p>A minister of the Gospel of our Lord Jesus Christ, Apostle Annan leads the ministry with a deep prophetic and apostolic grace, and a heart to see faith demonstrated in everyday lives.</p>
      </div>
    </article>
    <article class="leader">
      <img src="assets/natalie-annan.jpg" alt="Rev. Mrs Natalie Annan" width="440" height="440" loading="lazy">
      <div class="leader-text">
        <p class="role">Ministers alongside the Apostle</p>
        <h2>Rev. Mrs Natalie Annan</h2>
        <p>Rev. Mrs Annan serves alongside the Apostle, caring for the church family and ministering in worship and the Word.</p>
      </div>
    </article>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    <div class="sec-head"><h2>Ministry team</h2></div>
    <div class="team">
{team_cards}
    </div>
  </div>
</section>

<section class="feature-band">
  <img src="assets/photos/clergy-vestments.jpg" alt="Two ministers in clerical robes at FDMI" loading="lazy" style="object-position:50% 20%">
  <div class="feature-band-text">
    <h2>Set apart to serve</h2>
    <p>Our ministers are prayed over and set apart before the congregation, so the whole church stands with them in the work God has given them.</p>
  </div>
</section>''')

min_rows = "\n".join(f'''    <article class="ministry" id="{mid}">
      <img src="{img}" alt="" loading="lazy" style="object-position:{pos}">
      <div class="ministry-text">
        <h2>{name}</h2>
        <p>{text}</p>
        <a class="text-link" href="{wa(msg)}">Get involved</a>
      </div>
    </article>''' for mid, name, img, pos, text, msg in MINISTRIES)

pages["ministries.html"] = page("ministries.html", "Ministries",
    "Worship, prayer, youth, children, and outreach and welfare at Faith Demonstration Ministries International, Adjen-Kotoku, Accra.",
    f'''{page_head("Ministries", "There is a place for everyone to serve. Read about each ministry, then message us on WhatsApp to get involved.")}

<div class="container">
  <nav class="jump" aria-label="Ministries on this page">
    {"".join(f'<a href="#{m[0]}">{m[1]}</a>' for m in MINISTRIES)}
  </nav>
</div>

<section class="section section-top-tight">
  <div class="container ministries">
{min_rows}
  </div>
</section>''')

platform_notes = ["Services and messages", "Live services and clips", "Photos and short clips", "Short clips from services"]
pages["sermons.html"] = page("sermons.html", "Sermons",
    "Watch and listen to messages from Faith Demonstration Ministries International, or join us for Divine Service on Sundays and Study His Word on Tuesdays.",
    f'''{page_head("Sermons", "Messages from Divine Service and Study His Word. Watch online, or join us in person.")}

<section class="section section-top-tight">
  <div class="container split split-even">
    <div>
      <h2 class="h-sm">Watch and listen</h2>
      <ul class="platforms">
{chr(10).join(f'        <li><a href="{u}"><span class="platform-name">{n}</span><span class="platform-note">{note}</span></a></li>' for (n, u), note in zip(SOCIAL, platform_notes))}
      </ul>
    </div>
    <div>
      <h2 class="h-sm">Hear the Word in person</h2>
      <ul class="times">
        <li><span class="t-day">Sunday</span><span class="t-name">Divine Service</span><span class="t-time">8:30 – 11:00 AM</span></li>
        <li><span class="t-day">Tuesday</span><span class="t-name">Study His Word</span><span class="t-time">6:00 – 8:30 PM</span></li>
      </ul>
      <p class="note">Recorded messages are shared on our pages after services. Follow us to see them first.</p>
    </div>
  </div>
</section>

<section class="feature-band">
  <img src="assets/photos/congregation-joy.jpg" alt="The congregation rejoicing during a service" loading="lazy" style="object-position:50% 30%">
  <div class="feature-band-text">
    <h2>The undiluted Word</h2>
    <p>Preaching the undiluted Word of God is the first part of our mission. Every message points to Jesus and to faith that is lived out.</p>
  </div>
</section>''')

pages["events.html"] = page("events.html", "Events",
    "At His Feet: worship all night on Friday 4 December 2026 from 8:00 PM at FDMI, Adjen-Kotoku, Accra. Plus our weekly meetings.",
    f'''{page_head("Events", "Special services and the weekly meetings of the church.")}

<section class="section section-top-tight">
  <div class="container">
    {event_feature(full=True)}
  </div>
</section>

<section class="section section-tint">
  <div class="container split split-even">
    <div>
      <h2>Every week</h2>
      <p>All meetings hold at the church premises, last stop Adjen-Kotoku.</p>
    </div>
    {times_list()}
  </div>
</section>
{LIGHTBOX}''')

pages["announcements.html"] = page("announcements.html", "Announcements",
    "News and announcements from Faith Demonstration Ministries International, Adjen-Kotoku, Accra.",
    f'''{page_head("Announcements", "News for the church family. For anything else, call or message the church.")}

<section class="section section-top-tight">
  <div class="container notices-page">
{chr(10).join(announcement(a) for a in ANNOUNCEMENTS)}
  </div>
</section>''')

pages["visit.html"] = page("visit.html", "Plan a visit",
    f"Visit Faith Demonstration Ministries International: {ADDRESS}. Service times, directions and contacts.",
    f'''{page_head("Plan a visit", "We'd love to welcome you. Here is everything you need for your first visit.")}

<section class="section section-top-tight">
  <div class="container split split-even">
    <div>
      <h2 class="h-sm">Service times</h2>
      {times_list()}
    </div>
    <div>
      <h2 class="h-sm">Address</h2>
      <p class="address">{ADDRESS}, Ghana</p>
      <p>Call {phones_html()}<br>WhatsApp <a href="{WA}">059 660 9093</a></p>
      <div class="actions">
        <a class="btn btn-dark" href="{DIRECTIONS}">Get directions</a>
        <a class="btn btn-line" href="{WA}">Message us</a>
      </div>
    </div>
  </div>
</section>

<div class="container">
  {MAP}
</div>

<section class="section">
  <div class="container prose-grid">
    <h2>Your first visit</h2>
    <div class="prose">
      <p>You'll be greeted at the door and helped to a seat. Services include worship, prayer and the preaching of the Word.</p>
      <p>Children are part of the church family and are welcome at every service.</p>
      <p>If you would like prayer, tell an usher or send us a message before you come.</p>
      <a class="text-link" href="{wa("Hello, I would like to send a prayer request.")}">Send a prayer request</a>
    </div>
  </div>
</section>''')

pages["gallery.html"] = page("gallery.html", "Gallery",
    "Photos and video from worship, prayer, celebrations and church life at Faith Demonstration Ministries International, Accra.",
    f'''{page_head("Gallery", "Worship, prayer, celebrations and the FDMI family. Select a photo to view it full size.")}

<section class="section section-top-tight">
  <div class="container">
    <div class="gallery">
{chr(10).join(gallery_fig(f, c) for f, c in GALLERY)}
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="container split split-even">
    <div>
      <h2>Video</h2>
      <p>Our children dancing for joy at a church celebration.</p>
    </div>
    {VIDEO}
  </div>
</section>
{LIGHTBOX}''')

out = Path(__file__).parent
for name, html in pages.items():
    (out / name).write_text(html)
    print("wrote", name)
