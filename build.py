#!/usr/bin/env python3
"""Builds the static pages of the FDMI website.

All pages share one header and footer, defined here once.
Edit the content below, then run:  python3 build.py
Don't edit the generated .html files by hand.
"""
from pathlib import Path
from urllib.parse import quote

SITE = "https://fdmi-church.vercel.app"
WA_NUM = "233596609093"
WA = f"https://wa.me/{WA_NUM}"
PHONES = [("059 660 9093", "+233596609093"), ("020 171 3589", "+233201713589")]
ADDRESS = "Last stop, Adjen-Kotoku, next to Pick N Nikki School, Accra"
LAT, LNG = "5.74170883", "-0.35696792"  # from GhanaPostGPS GW-0706-5202
GPS = "GW-0706-5202"
GPS_URL = "https://ghanapostgps.com/map/?gps=GW07065202"
DIRECTIONS = f"https://www.google.com/maps/dir/?api=1&amp;destination={LAT},{LNG}"
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


def slug(t):
    import re
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def strip_tags(h):
    import re
    return re.sub(r"<[^>]+>", "", h)


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
      <p>GhanaPostGPS <a href="{GPS_URL}">{GPS}</a></p>
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

SUMMARIES = {  # short versions of announcements for the home page
    "At His Feet: worship all night": "A night of worship on Friday 4 December from 8:00 PM. Everyone is welcome.",
    "Church building project": "We are raising support to build a permanent home for the church.",
    "Send your prayer requests": "Send a prayer request at any time on WhatsApp.",
}

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
    ("hands-raised", "Hands raised in worship"),
    ("sunday-service", "A Sunday service"),
    ("fellowship-in-white", "Fellowship in white"),
    ("studio-visit", "At the studio"),
]

TEAM = [  # (photo, position, name) - add names when confirmed
    ("assets/people/church-elder.jpg", "Church Elder", ""),
    ("assets/people/church-secretary.jpg", "Church Secretary", ""),
]


NAME = "Faith Demonstration Ministries International"
SHORT = "FDMI"
LOCALITY = "Adzen (Adjen-Kotoku), Ga West, Accra"

TITLES = {  # page title tags, kept under ~60 characters for search results
    "index.html": "Faith Demonstration Ministries International, Accra",
    "about.html": "About FDMI | Vision, Mission and Goals",
    "leaders.html": "Leaders | Apostle Victor Annan | FDMI Accra",
    "ministries.html": "Ministries | Worship, Prayer, Youth, Children | FDMI",
    "sermons.html": "Sermons | Divine Service and Study His Word | FDMI",
    "events.html": "At His Feet All-Night Worship, 4 Dec 2026 | FDMI",
    "announcements.html": "Announcements | FDMI Church, Adjen-Kotoku, Accra",
    "visit.html": "Service Times and Directions | FDMI Church, Accra",
    "gallery.html": "Photos and Video | FDMI Church, Accra",
}

CRUMB = {"about.html": "About", "leaders.html": "Leaders", "ministries.html": "Ministries", "sermons.html": "Sermons",
         "events.html": "Events", "announcements.html": "Announcements", "visit.html": "Plan a visit", "gallery.html": "Gallery"}


def church_ld():
    import json
    days = {0: "Sunday", 2: "Tuesday", 3: "Wednesday", 5: "Friday"}
    return {
        "@type": ["Church", "PlaceOfWorship"],
        "@id": f"{SITE}/#church",
        "name": NAME,
        "alternateName": SHORT,
        "description": "A prophetic and apostolic church in Adzen (Adjen-Kotoku), Ga West, Accra, Ghana, led by Apostle Victor Annan.",
        "url": f"{SITE}/",
        "logo": f"{SITE}/assets/fdmi-crest.jpg",
        "image": [f"{SITE}/assets/photos/worship-team.jpg", f"{SITE}/assets/photos/church-family.jpg"],
        "telephone": PHONES[0][1],
        "contactPoint": [{"@type": "ContactPoint", "telephone": t, "contactType": "customer service", "areaServed": "GH",
                          "availableLanguage": ["en"]} for _, t in PHONES],
        "address": {"@type": "PostalAddress",
                    "streetAddress": "Last stop, Adjen-Kotoku, next to Pick N Nikki School",
                    "addressLocality": "Adzen, Ga West", "addressRegion": "Greater Accra",
                    "postalCode": "GW-0706-5202", "addressCountry": "GH"},
        "geo": {"@type": "GeoCoordinates", "latitude": float(LAT), "longitude": float(LNG)},
        "hasMap": f"https://www.google.com/maps?q={LAT},{LNG}",
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": f"https://schema.org/{days[d]}",
             "opens": o, "closes": c, "description": m}
            for d, m, o, c in [(0, "Divine Service", "08:30", "11:00"), (2, "Study His Word", "18:00", "20:30"),
                               (3, "Grace Hour", "09:00", "12:00"), (5, "Liberation and Prophetic Hour", "18:30", "21:00")]],
        "member": [{"@type": "Person", "name": "Apostle Victor Annan", "jobTitle": "Head of the ministry"},
                   {"@type": "Person", "name": "Rev. Mrs Natalie Annan", "jobTitle": "Minister"}],
        "sameAs": ["https://www.instagram.com/apostlevictorannan", "https://www.tiktok.com/@apostlevictorannan", GPS_URL],
        "slogan": "To raise an indigenous and self-supporting church, and to demonstrate the love of God in our generation.",
    }


def event_ld():
    e = EVENT
    return {
        "@type": "Event", "@id": f"{SITE}/events.html#at-his-feet",
        "name": "At His Feet: Worship All Night",
        "description": f"An all-night worship service at {NAME} with {e['with']}.",
        "startDate": "2026-12-04T20:00:00+00:00", "endDate": "2026-12-05T05:00:00+00:00",
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "image": [f"{SITE}/assets/at-his-feet-flyer.jpg"],
        "location": {"@id": f"{SITE}/#church"},
        "organizer": {"@id": f"{SITE}/#church"},
        "performer": [{"@type": "Person", "name": n.strip()} for n in e["with"].replace(" and ", ", ").split(",")],
    }


def page(file, title, desc, body, og=None, preload=None, extra_ld=None):
    import json
    full = TITLES.get(file, f"{title} | {NAME}")
    url = SITE + "/" + ("" if file == "index.html" else file)
    og_img = f"{SITE}/assets/og/{file.replace('.html', '')}.jpg"
    graph = [church_ld(), {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": NAME,
                           "alternateName": SHORT, "inLanguage": "en-GH", "publisher": {"@id": f"{SITE}/#church"}},
             {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": full, "description": desc,
              "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#church"},
              "primaryImageOfPage": og_img, "inLanguage": "en-GH"}]
    if file != "index.html":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": CRUMB[file], "item": url}]})
    graph += extra_ld or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    pre = f'\n<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f'''<!DOCTYPE html>
<html lang="en-GH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#1d1915">
<link rel="canonical" href="{url}">
<meta name="geo.region" content="GH-AA">
<meta name="geo.placename" content="{LOCALITY}">
<meta name="geo.position" content="{LAT};{LNG}">
<meta name="ICBM" content="{LAT}, {LNG}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_GH">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:secure_url" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}, {NAME}, Adjen-Kotoku, Accra">
<meta property="place:location:latitude" content="{LAT}">
<meta property="place:location:longitude" content="{LNG}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<meta name="twitter:image:alt" content="{title}, {NAME}">
<link rel="icon" href="assets/fdmi-crest.jpg">
<link rel="apple-touch-icon" href="assets/fdmi-crest.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>{pre}
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Schibsted+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">
{ld}
</script>
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


def event_feature(mode="full"):
    e = EVENT
    full = mode == "full"
    extra = f'''
        <p class="event-with"><span>Ministering</span> {e["with"]}</p>'''
    if full:
        actions = f'''
        <div class="actions">
          <a class="btn btn-dark" data-ics href="#" download="at-his-feet.ics">Add to calendar</a>
          <a class="btn btn-line" href="tel:{PHONES[0][1]}">Call {PHONES[0][0]}</a>
        </div>'''
    else:
        actions = '''
        <div class="actions">
          <a class="btn btn-dark" href="events.html">Event details</a>
          <a class="btn btn-line" data-ics href="#" download="at-his-feet.ics">Add to calendar</a>
        </div>'''
    return f'''<article class="event event-full" id="at-his-feet" data-start="{e["start"]}" data-end="{e["end"]}">
      <a class="event-flyer" href="assets/at-his-feet-flyer.jpg" data-lightbox>
        <img src="assets/at-his-feet-flyer.jpg" alt="At His Feet flyer: worship all night, Friday 4th December 2026, 8:00 PM" width="720" height="1007" loading="lazy">
      </a>
      <div class="event-body">
        <p class="event-date"><time datetime="2026-12-04T20:00">{e["date"]}</time><span data-countdown></span></p>
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
    more = f'<a class="btn btn-line btn-sm" href="{link[0]}">{link[1]}</a>' if link else ""
    if compact:
        return f'''          <li class="notice">
            <p class="notice-date">{date}</p>
            <p class="notice-title">{title}</p>
          </li>'''
    return f'''    <article class="notice-full" id="{slug(title)}">
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

MAP = f'''<div class="map">
    <iframe title="Map showing Faith Demonstration Ministries International, Adzen, Ga West" src="https://maps.google.com/maps?q={LAT},{LNG}&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>'''

# ---------------------------------------------------------------- pages
pages = {}

def head_c(kicker, title, sub=""):
    sub_html = f'\n      <p class="head-sub">{sub}</p>' if sub else ""
    return f'''<header class="head-c">
      <p class="kicker">{kicker}</p>
      <h2>{title}</h2>{sub_html}
    </header>'''


ICONS = {
    "about": '<path d="M3 21h18M5 21V10l7-5 7 5v11"/><path d="M10 21v-5h4v5M12 3v3"/>',
    "leaders": '<circle cx="12" cy="7" r="3.5"/><path d="M5 21a7 7 0 0 1 14 0"/>',
    "ministries": '<circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2 20a6 6 0 0 1 12 0M10 20a6 6 0 0 1 12 0"/>',
    "sermons": '<path d="M4 5h7a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H4zM20 5h-5a2 2 0 0 0-2 2"/><path d="M20 5v13h-5"/>',
    "announcements": '<path d="M3 11v2a1 1 0 0 0 1 1h3l6 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M17 8a5 5 0 0 1 0 8"/>',
    "gallery": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-8 8"/>',
}
EXPLORE = [("about.html", "About us", "about"), ("leaders.html", "Leaders", "leaders"), ("ministries.html", "Ministries", "ministries"),
           ("sermons.html", "Sermons", "sermons"), ("announcements.html", "Announcements", "announcements"), ("gallery.html", "Gallery", "gallery")]

home_rows = "\n".join(f'''        <tr data-day="{n}"><th scope="row">{d}</th><td>{m}</td><td class="t-time">{t}</td></tr>''' for n, d, m, t in SERVICES)

pages["index.html"] = page("index.html", "Home",
    "A prophetic and apostolic church in Adjen-Kotoku (Adzen), Accra, led by Apostle Victor Annan. Sunday Divine Service at 8:30 AM. Everyone is welcome.",
    f'''<section class="hero" aria-label="Welcome">
  <div class="hero-slides" aria-label="Photos from FDMI">
    <img class="hero-slide is-active" src="assets/photos/worship-team.jpg" alt="The worship team leading praise in front of the gold F D M I letters" style="object-position:50% 40%" fetchpriority="high">
    <img class="hero-slide" src="assets/photos/consecration.jpg" alt="Apostle Victor Annan ministering at a consecration service" style="object-position:50% 22%">
    <img class="hero-slide" src="assets/photos/church-family.jpg" alt="The FDMI church family together" style="object-position:50% 35%">
    <img class="hero-slide" src="assets/photos/white-service-2.jpg" alt="The congregation in prayer under the F D M I letters" style="object-position:40% 50%">
    <img class="hero-slide" src="assets/photos/clergy-vestments.jpg" alt="FDMI ministers in their robes" style="object-position:50% 20%">
    <img class="hero-slide" src="assets/photos/sunday-service.jpg" alt="Ministry during a Sunday service" style="object-position:40% 50%">
  </div>
  <div class="hero-dots"><button type="button" aria-label="Show photo 1" aria-current="true"></button><button type="button" aria-label="Show photo 2"></button><button type="button" aria-label="Show photo 3"></button><button type="button" aria-label="Show photo 4"></button><button type="button" aria-label="Show photo 5"></button><button type="button" aria-label="Show photo 6"></button></div>
  <div class="container hero-content">
    <img class="hero-crest" src="assets/fdmi-crest.jpg" alt="" width="76" height="76">
    <p class="kicker kicker-light">You are welcome</p>
    <h1>Faith Demonstration<br><span>Ministries International</span></h1>
    <p class="hero-sub">A prophetic and apostolic church &middot; Adjen-Kotoku, Accra</p>
    <p class="hero-copy">Led by Apostle Victor Annan. Our Divine Service is every Sunday from 8:30 AM. Come and worship with us. Everybody is welcome.</p>
    <div class="hero-actions">
      <a class="btn btn-gold btn-lg" href="visit.html">Plan your visit</a>
      <a class="btn btn-ghost btn-lg" href="#times">Service times</a>
    </div>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("What we're about", "A church built on the Word and the Spirit", "Everything we do comes from the Word of God and is led by the Holy Spirit.")}
    <div class="img-cards">
{chr(10).join(f'      <a class="card img-card" href="ministries.html#{m[0]}"><img src="{m[2]}" alt="" loading="lazy" style="object-position:{m[3]}"><span>{m[1]}</span></a>' for m in MINISTRIES[:4])}
    </div>
    <div class="h-actions"><a class="btn btn-outline" href="ministries.html">Explore our ministries</a></div>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    <article class="card leader-card">
      <a href="leaders.html" class="leader-card-img" tabindex="-1" aria-hidden="true"><img src="assets/photos/consecration.jpg" alt="" loading="lazy"></a>
      <div class="card-body">
        <p class="kicker kicker-left">Our leadership</p>
        <h2>Apostle Victor Annan</h2>
        <p>Apostle Victor Annan leads the ministry with a deep prophetic and apostolic grace. Rev. Mrs Natalie Annan ministers alongside him, with a team of elders and officers serving the church family.</p>
        <ul class="faces" aria-hidden="true">
          <li><img src="assets/victor-annan.jpg" alt="" loading="lazy"></li>
          <li><img src="assets/natalie-annan.jpg" alt="" loading="lazy"></li>
{chr(10).join(f'          <li><img src="{t[0]}" alt="" loading="lazy"></li>' for t in TEAM)}
        </ul>
        <a class="btn btn-outline" href="leaders.html">Meet our leaders</a>
      </div>
    </article>

    <article class="card sermon-card">
      <a href="sermons.html" class="sermon-card-img" tabindex="-1" aria-hidden="true"><img src="assets/photos/hands-raised.jpg" alt="" loading="lazy"></a>
      <div class="card-body card-dark">
        <p class="kicker kicker-left kicker-light">Sermons</p>
        <h2>Grow in the Word</h2>
        <p>Hear the undiluted Word of God every Sunday at Divine Service and every Tuesday at Study His Word, or catch up online.</p>
        <a class="btn btn-white" href="sermons.html">Watch sermons and messages</a>
      </div>
    </article>
  </div>
</section>

<section class="h-sec h-tint" id="times">
  <div class="narrow">
    {head_c("Join us this week", "Our service times", "All our meetings hold at the church premises, last stop Adjen-Kotoku, Accra.")}
    <div class="card table-card">
      <table class="times-table">
        <thead><tr><th scope="col">Day</th><th scope="col">Meeting</th><th scope="col">Time</th></tr></thead>
        <tbody>
{home_rows}
        </tbody>
      </table>
    </div>
    <p class="table-note">Call {phones_html()} for special programmes.</p>
    <a class="btn btn-dark btn-block" href="visit.html">Plan your visit</a>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    {head_c("Discover more", "Explore FDMI")}
    <div class="explore">
{chr(10).join(f'      <a class="card explore-item" href="{h}"><span class="explore-icon{" explore-gold" if i % 2 else ""}"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[ic]}</svg></span>{l}</a>' for i, (h, l, ic) in enumerate(EXPLORE))}
    </div>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    <article class="card event-card" data-start="{EVENT["start"]}" data-end="{EVENT["end"]}">
      <a class="event-card-img" href="assets/at-his-feet-flyer.jpg" data-lightbox><img src="assets/at-his-feet-flyer.jpg" alt="At His Feet flyer: worship all night, Friday 4th December 2026, 8:00 PM" loading="lazy"></a>
      <div class="card-body">
        <p class="kicker kicker-left">Save the date</p>
        <h2>At His Feet</h2>
        <p class="event-when"><time datetime="2026-12-04T20:00">{EVENT["date"]}, from 8:00 PM</time> <span data-countdown></span></p>
        <p>A night of worship at the church premises with Bishop Victor Annan, Rev. Mrs Natalie Annan, Rose Adjei, Anita Binney and other ministers.</p>
        <a class="btn btn-dark btn-block" href="events.html">View all events</a>
        <a class="btn btn-outline btn-block" data-ics href="#" download="at-his-feet.ics">Add to calendar</a>
      </div>
    </article>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    {head_c("News", "Announcements", "The latest from the church family.")}
    <div class="card list-card">
{chr(10).join(f"""      <a class="list-row" href="announcements.html#{slug(a[1])}">
        <span class="list-date">{a[0]}</span>
        <span class="list-text"><strong>{a[1]}</strong>{SUMMARIES.get(a[1], strip_tags(a[2]))}</span>
      </a>""" for a in ANNOUNCEMENTS[:3])}
    </div>
    <a class="btn btn-dark btn-block" href="announcements.html">Read all announcements</a>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Find us", "Where we are")}
    <article class="card find-card">
      {MAP}
      <div class="card-body">
        <h3>Find us in Adjen-Kotoku</h3>
        <dl class="facts">
          <div><dt>Address</dt><dd>{ADDRESS}</dd></div>
          <div><dt>GhanaPostGPS</dt><dd><a href="{GPS_URL}">{GPS}</a></dd></div>
          <div><dt>Landmark</dt><dd>Next to Pick N Nikki School</dd></div>
          <div><dt>Phone</dt><dd>{phones_html()}</dd></div>
          <div><dt>WhatsApp</dt><dd><a href="{WA}">059 660 9093</a></dd></div>
        </dl>
        <a class="btn btn-outline btn-block" href="{DIRECTIONS}">Get directions on Google Maps</a>
        <a class="btn btn-dark btn-block" href="visit.html">Plan your visit</a>
      </div>
    </article>

    <a class="card gallery-card" href="gallery.html">
      <img src="assets/photos/church-family.jpg" alt="The FDMI family together in front of the church banner" loading="lazy">
      <span class="btn btn-white">View gallery</span>
    </a>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    <figure class="card quote-card">
      <p class="kicker">Why we're called Faith Demonstration</p>
      <blockquote>My message and my preaching were not with wise and persuasive words, but with a demonstration of the Spirit's power, so that your faith might not rest on human wisdom, but on God's power.</blockquote>
      <figcaption>1 Corinthians 2:4–5</figcaption>
    </figure>
    <div class="h-actions"><a class="btn btn-dark btn-lg" href="{wa("Hello, I would like to send a prayer request.")}">Send a prayer request</a></div>
  </div>
</section>
{LIGHTBOX}''', preload="assets/photos/worship-team.jpg")


def page_hero(img, pos, kicker, title, sub):
    return f'''<section class="page-hero">
  <img class="page-hero-img" src="{img}" alt="" style="object-position:{pos}" fetchpriority="high">
  <div class="narrow page-hero-body">
    <p class="kicker kicker-light">{kicker}</p>
    <h1>{title}</h1>
    <p>{sub}</p>
  </div>
</section>'''


def cta(title, text, href, label, alt_href=None, alt_label=None):
    alt = f'\n        <a class="btn btn-ghost" href="{alt_href}">{alt_label}</a>' if alt_href else ""
    return f'''<section class="h-sec">
  <div class="narrow">
    <div class="cta-box">
      <h2>{title}</h2>
      <p>{text}</p>
      <div class="cta-actions">
        <a class="btn btn-gold" href="{href}">{label}</a>{alt}
      </div>
    </div>
  </div>
</section>'''


def times_card(rows=None):
    rows = rows or SERVICES
    body = "\n".join(f'        <tr data-day="{n}"><th scope="row">{d}</th><td>{m}</td><td class="t-time">{t}</td></tr>' for n, d, m, t in rows)
    return f'''<div class="card table-card">
      <table class="times-table">
        <thead><tr><th scope="col">Day</th><th scope="col">Meeting</th><th scope="col">Time</th></tr></thead>
        <tbody>
{body}
        </tbody>
      </table>
    </div>'''


PRAYER_CTA = cta("Need prayer?", "Send your prayer request on WhatsApp at any time. Our ministers pray over every request.",
                 wa("Hello, I would like to send a prayer request."), "Send a prayer request", "visit.html", "Plan a visit")

# ---------------------------------------------------------------- About
pages["about.html"] = page("about.html", "About the church",
    "Our vision is to raise an indigenous and self-supporting church and to demonstrate the love of God in our generation. Read FDMI's mission, focus and goals.",
    f'''{page_hero("assets/photos/church-family.jpg", "50% 30%", "About the church", "A family of faith in Adjen-Kotoku", "A prophetic and apostolic church in Accra, Ghana, led by Apostle Victor Annan.")}

<section class="h-sec">
  <div class="narrow">
    <article class="card split-card">
      <div class="split-card-img"><img src="assets/photos/sunday-service.jpg" alt="Ministry during a Sunday service at FDMI" loading="lazy" style="object-position:35% 50%"></div>
      <div class="card-body">
        <p class="kicker kicker-left">Who we are</p>
        <h2>Faith that is shown, not only spoken</h2>
        <p>We gather to worship, to hear the undiluted Word of God and to see it at work in everyday lives: in healing, in restoration and in families made whole.</p>
        <p>Whether you have walked with Jesus for years or are only beginning to ask questions, there is a seat for you in the house.</p>
      </div>
    </article>
  </div>
</section>

<section class="h-sec h-dark">
  <div class="narrow center">
    <p class="kicker kicker-light">Our vision</p>
    <p class="vision-statement">To raise an indigenous and self&#8209;supporting church, and to demonstrate the love of God in our generation.</p>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("What drives us", "Mission, focus and goals")}
    <div class="three-cards">
      <article class="card text-card">
        <h3>Our mission</h3>
        <ol class="num-list">
          <li>To preach the undiluted Word of God.</li>
          <li>Spiritual growth, numerical growth and financial growth.</li>
          <li>Equipping the saints of Christ (Ephesians 4:11–13).</li>
        </ol>
      </article>
      <article class="card text-card">
        <h3>Our focus</h3>
        <p>The sub-communities around us, the youth and the children, training them with vocational skills.</p>
      </article>
      <article class="card text-card">
        <h3>Our goals</h3>
        <ol class="num-list">
          <li>To reach the unreached.</li>
          <li>To help the less privileged.</li>
          <li>To help the aged.</li>
        </ol>
      </article>
    </div>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    <figure class="card quote-card">
      <p class="kicker">Our name</p>
      <blockquote>My message and my preaching were not with wise and persuasive words, but with a demonstration of the Spirit's power, so that your faith might not rest on human wisdom, but on God's power.</blockquote>
      <figcaption>1 Corinthians 2:4–5</figcaption>
    </figure>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Life at FDMI", "Worship, Word and family")}
    <div class="img-cards">
      <a class="card img-card" href="ministries.html#worship"><img src="assets/photos/worship-team.jpg" alt="" loading="lazy" style="object-position:50% 45%"><span>Worship</span></a>
      <a class="card img-card" href="sermons.html"><img src="assets/photos/hands-raised.jpg" alt="" loading="lazy"><span>The Word</span></a>
      <a class="card img-card" href="ministries.html#prayer"><img src="assets/photos/white-service-4.jpg" alt="" loading="lazy"><span>Prayer</span></a>
      <a class="card img-card" href="ministries.html#children"><img src="assets/photos/child-dedication.jpg" alt="" loading="lazy" style="object-position:50% 25%"><span>Family</span></a>
    </div>
    <div class="h-actions"><a class="btn btn-dark" href="leaders.html">Meet our leaders</a></div>
  </div>
</section>

{PRAYER_CTA}''')

# ---------------------------------------------------------------- Leaders
def profile(img, pos, role, name, text, flip=False):
    return f'''<article class="card profile-card{' profile-flip' if flip else ''}">
      <div class="profile-img"><img src="{img}" alt="{name}" loading="lazy" style="object-position:{pos}"></div>
      <div class="card-body">
        <p class="kicker kicker-left">{role}</p>
        <h2>{name}</h2>
        <p>{text}</p>
      </div>
    </article>'''


members = "\n".join(f'''      <figure class="card member-card">
        <img src="{img}" alt="{name or 'FDMI ' + role}" loading="lazy">
        <figcaption><strong>{name or role}</strong>{f"<span>{role}</span>" if name else "<span>Faith Demonstration Ministries International</span>"}</figcaption>
      </figure>''' for img, role, name in TEAM)

pages["leaders.html"] = page("leaders.html", "Leaders",
    "Meet the leadership of Faith Demonstration Ministries International: Apostle Victor Annan, Rev. Mrs Natalie Annan and the ministry team.",
    f'''{page_hero("assets/photos/consecration.jpg", "50% 25%", "Our leadership", "Shepherds of the house", "The men and women God has given to lead and care for the FDMI family.")}

<section class="h-sec">
  <div class="narrow">
    {head_c("Leadership", "Our pastors")}
    {profile("assets/victor-annan.jpg", "50% 15%", "Head of the ministry", "Apostle Victor Annan", "A minister of the Gospel of our Lord Jesus Christ, Apostle Annan leads the ministry with a deep prophetic and apostolic grace, and a heart to see faith demonstrated in everyday lives.")}
    {profile("assets/natalie-annan.jpg", "50% 20%", "Ministers alongside the Apostle", "Rev. Mrs Natalie Annan", "Rev. Mrs Annan serves alongside the Apostle, caring for the church family and ministering in worship and the Word.", flip=True)}
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Ministry team", "Serving the FDMI family", "The elders and officers who keep the house running, week by week.")}
    <div class="member-grid">
{members}
    </div>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    <article class="card split-card">
      <div class="split-card-img"><img src="assets/photos/clergy-vestments.jpg" alt="Two ministers in clerical robes at FDMI" loading="lazy" style="object-position:50% 18%"></div>
      <div class="card-body">
        <p class="kicker kicker-left">Called and consecrated</p>
        <h2>Set apart to serve</h2>
        <p>Our ministers are prayed over and set apart before the congregation, so the whole church stands with them in the work God has given them.</p>
        <a class="btn btn-outline" href="gallery.html">See the gallery</a>
      </div>
    </article>
  </div>
</section>

{cta("Speak with a leader", "To arrange a meeting, counselling or prayer with one of our pastors, call or send us a message.", WA, "Message us on WhatsApp", f"tel:{PHONES[0][1]}", f"Call {PHONES[0][0]}")}''')

# ---------------------------------------------------------------- Ministries
min_cards = "\n".join(f'''      <article class="card ministry-card" id="{mid}">
        <img src="{img}" alt="" loading="lazy" style="object-position:{pos}">
        <div class="card-body">
          <h2>{name}</h2>
          <p>{text}</p>
          <a class="btn btn-outline" href="{wa(msg)}">Get involved</a>
        </div>
      </article>''' for mid, name, img, pos, text, msg in MINISTRIES)

pages["ministries.html"] = page("ministries.html", "Ministries",
    "Worship, prayer, youth, children, and outreach and welfare at Faith Demonstration Ministries International, Adjen-Kotoku, Accra.",
    f'''{page_hero("assets/photos/youth-night.jpg", "50% 40%", "Ministries", "A place for everyone to serve", "Find where you fit, then message us on WhatsApp to get involved.")}

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Our ministries", "Serve with us")}
    <div class="ministry-grid">
{min_cards}
    </div>
  </div>
</section>

{cta("Not sure where you fit?", "Tell us a little about yourself and we will help you find the right ministry.", wa("Hello, I would like to serve at FDMI."), "Message us on WhatsApp")}''')

# ---------------------------------------------------------------- Sermons
PLATFORM_ICONS = {
    "YouTube": '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M10 9l5 3-5 3z" fill="currentColor"/>',
    "Facebook": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8z"/>',
    "Instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>',
    "TikTok": '<path d="M14 3v11a4 4 0 1 1-4-4"/><path d="M14 3c0 3 2 5 5 5"/>',
}
platform_cards = "\n".join(f'''      <a class="card platform-card" href="{u}">
        <span class="explore-icon{" explore-gold" if i % 2 else ""}"><svg viewBox="0 0 24 24" aria-hidden="true">{PLATFORM_ICONS[n]}</svg></span>
        <strong>{n}</strong>
        <span>{note}</span>
      </a>''' for i, ((n, u), note) in enumerate(zip(SOCIAL, ["Services and messages", "Live services and clips", "Photos and short clips", "Short clips from services"])))

pages["sermons.html"] = page("sermons.html", "Sermons",
    "Watch and listen to messages from Faith Demonstration Ministries International, or join us for Divine Service on Sundays and Study His Word on Tuesdays.",
    f'''{page_hero("assets/photos/hands-raised.jpg", "50% 40%", "Sermons", "Grow in the Word", "Messages from Divine Service and Study His Word. Watch online, or join us in person.")}

<section class="h-sec">
  <div class="narrow">
    <article class="card sermon-card">
      <div class="sermon-card-img"><img src="assets/photos/sunday-service.jpg" alt="Ministry during a Sunday service" loading="lazy" style="object-position:40% 50%"></div>
      <div class="card-body card-dark">
        <p class="kicker kicker-left kicker-light">The undiluted Word</p>
        <h2>Preaching that points to Jesus</h2>
        <p>Preaching the undiluted Word of God is the first part of our mission. Every message points to Jesus and to faith that is lived out.</p>
        <a class="btn btn-white" href="{SOCIAL[0][1]}">Watch on YouTube</a>
      </div>
    </article>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Online", "Watch and listen", "Recorded messages are shared on our pages after services.")}
    <div class="platform-grid">
{platform_cards}
    </div>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    {head_c("In person", "Hear the Word with us", "Teaching services at the church premises, last stop Adjen-Kotoku.")}
    {times_card([s for s in SERVICES if s[0] in (0, 2)])}
    <div class="h-actions"><a class="btn btn-dark" href="visit.html">Plan your visit</a></div>
  </div>
</section>''')

# ---------------------------------------------------------------- Events
e = EVENT
ministers = "".join(f"<li>{n.strip()}</li>" for n in e["with"].replace(" and ", ", ").split(","))
pages["events.html"] = page("events.html", "Events",
    "At His Feet: worship all night on Friday 4 December 2026 from 8:00 PM at FDMI, Adjen-Kotoku, Accra. Plus our weekly meetings.",
    f'''{page_hero("assets/photos/night-prayer.jpg", "50% 35%", "Events", "What's coming up", "Special services, all-night worship and the weekly meetings of the church.")}

<section class="h-sec">
  <div class="narrow">
    {head_c("Next special service", "At His Feet", "Worship all night")}
    <article class="card event-page-card" id="at-his-feet" data-start="{e["start"]}" data-end="{e["end"]}">
      <a class="event-poster" href="assets/at-his-feet-flyer.jpg" data-lightbox>
        <img src="assets/at-his-feet-flyer.jpg" alt="At His Feet flyer: worship all night, Friday 4th December 2026, 8:00 PM" loading="lazy">
        <span class="poster-hint">View full flyer</span>
      </a>
      <div class="card-body">
        <p class="kicker kicker-left">Save the date</p>
        <div class="count-tiles" data-tiles aria-label="Time until the service">
          <div><b data-u="d">--</b><span>Days</span></div>
          <div><b data-u="h">--</b><span>Hours</span></div>
          <div><b data-u="m">--</b><span>Minutes</span></div>
        </div>
        <p class="count-msg" data-countdown></p>
        <dl class="facts event-facts">
          <div><dt>Date</dt><dd>{e["date"]}</dd></div>
          <div><dt>Time</dt><dd>{e["time"]}, all night</dd></div>
          <div><dt>Venue</dt><dd>{e["place"]}</dd></div>
          <div><dt>GPS</dt><dd><a href="{GPS_URL}">{GPS}</a></dd></div>
          <div><dt>Info</dt><dd>{phones_html()}</dd></div>
        </dl>
        <a class="btn btn-dark btn-block" data-ics href="#" download="at-his-feet.ics">Add to calendar</a>
        <a class="btn btn-outline btn-block" href="{DIRECTIONS}">Get directions</a>
      </div>
    </article>
    <div class="card ministers-card">
      <h3>Ministering on the night</h3>
      <ul class="chips">{ministers}</ul>
    </div>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Every week", "Our regular meetings", "All meetings hold at the church premises, last stop Adjen-Kotoku, Accra.")}
    {times_card()}
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    {head_c("Past services", "Moments from the house")}
    <div class="photo-row">
      <a class="card photo-tile" href="gallery.html"><img src="assets/photos/white-service-2.jpg" alt="A night of prayer at FDMI" loading="lazy"></a>
      <a class="card photo-tile" href="gallery.html"><img src="assets/photos/consecration.jpg" alt="Laying on of hands" loading="lazy" style="object-position:50% 25%"></a>
      <a class="card photo-tile" href="gallery.html"><img src="assets/photos/family-celebration.jpg" alt="Family celebration" loading="lazy" style="object-position:50% 30%"></a>
    </div>
    <div class="h-actions"><a class="btn btn-outline" href="gallery.html">Open the gallery</a></div>
  </div>
</section>

{cta("Bring someone with you", "Share this event with family and friends, or ask us about upcoming programmes.", wa("Hello, I would like to know about upcoming programmes at FDMI."), "Ask on WhatsApp")}
{LIGHTBOX}''', extra_ld=[event_ld()])

# ---------------------------------------------------------------- Announcements
ann_cards = "\n".join(f'''    <article class="card ann-card" id="{slug(t)}">
      <div class="ann-date">{d}</div>
      <div class="card-body">
        <h2>{t}</h2>
        <p>{b}</p>
        {f'<a class="btn btn-outline" href="{l[0]}">{l[1]}</a>' if l else ""}
      </div>
    </article>''' for d, t, b, l in ANNOUNCEMENTS)

pages["announcements.html"] = page("announcements.html", "Announcements",
    "News and announcements from Faith Demonstration Ministries International, Adjen-Kotoku, Accra.",
    f'''{page_hero("assets/photos/sunday-service.jpg", "40% 50%", "News", "Announcements", "News for the church family. For anything else, call or message the church.")}

<section class="h-sec h-tint">
  <div class="narrow ann-list">
{ann_cards}
  </div>
</section>

{PRAYER_CTA}''')

# ---------------------------------------------------------------- Visit
expect = [("A warm welcome", "You'll be greeted at the door and helped to a seat."),
          ("Worship and the Word", "Services include praise, prayer and the preaching of the Word."),
          ("Children welcome", "Children are part of the church family and welcome at every service."),
          ("Prayer for you", "Tell an usher if you would like prayer, or message us before you come.")]
pages["visit.html"] = page("visit.html", "Plan a visit",
    f"Visit Faith Demonstration Ministries International: {ADDRESS}. Service times, directions and contacts.",
    f'''{page_hero("assets/photos/white-service-1.jpg", "50% 45%", "Plan a visit", "We'd love to welcome you", "Everything you need for your first visit to FDMI.")}

<section class="h-sec" id="times">
  <div class="narrow">
    {head_c("Join us this week", "Service times", "All meetings hold at the church premises, last stop Adjen-Kotoku, Accra.")}
    {times_card()}
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Find us", "Where we are")}
    <article class="card find-card">
      {MAP}
      <div class="card-body">
        <h3>Find us in Adjen-Kotoku</h3>
        <dl class="facts">
          <div><dt>Address</dt><dd>{ADDRESS}</dd></div>
          <div><dt>Area</dt><dd>Adzen, Ga West, Greater Accra</dd></div>
          <div><dt>GhanaPostGPS</dt><dd><a href="{GPS_URL}">{GPS}</a></dd></div>
          <div><dt>Landmark</dt><dd>Next to Pick N Nikki School</dd></div>
          <div><dt>Phone</dt><dd>{phones_html()}</dd></div>
          <div><dt>WhatsApp</dt><dd><a href="{WA}">059 660 9093</a></dd></div>
        </dl>
        <a class="btn btn-dark btn-block" href="{DIRECTIONS}">Get directions on Google Maps</a>
        <a class="btn btn-outline btn-block" href="{WA}">Message us on WhatsApp</a>
      </div>
    </article>
  </div>
</section>

<section class="h-sec">
  <div class="narrow">
    {head_c("Your first visit", "What to expect")}
    <div class="expect-grid">
{chr(10).join(f'      <article class="card text-card"><h3>{t}</h3><p>{x}</p></article>' for t, x in expect)}
    </div>
  </div>
</section>

{PRAYER_CTA}''')

# ---------------------------------------------------------------- Gallery
pages["gallery.html"] = page("gallery.html", "Gallery",
    "Photos and video from worship, prayer, celebrations and church life at Faith Demonstration Ministries International, Accra.",
    f'''{page_hero("assets/photos/youth.jpg", "50% 35%", "Gallery", "Life in the house", "Worship, prayer, celebrations and the FDMI family. Select any photo to view it full size.")}

<section class="h-sec">
  <div class="narrow-wide">
    <div class="photo-grid">
{chr(10).join(f'      <figure class="card photo-frame"><a href="assets/photos/{f}.jpg" data-lightbox><img src="assets/photos/{f}.jpg" alt="{c}" loading="lazy"></a><figcaption>{c}</figcaption></figure>' for f, c in GALLERY)}
    </div>
  </div>
</section>

<section class="h-sec h-tint">
  <div class="narrow">
    {head_c("Video", "Children's celebration", "Our children dancing for joy at a church celebration.")}
    <div class="card video-card">
      <video controls preload="none" playsinline poster="assets/video/children-celebration.jpg">
        <source src="assets/video/children-celebration.mp4" type="video/mp4">
      </video>
    </div>
  </div>
</section>
{LIGHTBOX}''')


out = Path(__file__).parent
for name, html in pages.items():
    (out / name).write_text(html)
    print("wrote", name)

# ---------------------------------------------------------------- SEO files
from datetime import date
today_iso = date.today().isoformat()
priority = {"index.html": "1.0", "visit.html": "0.9", "events.html": "0.9", "about.html": "0.8", "sermons.html": "0.8"}
urls = "\n".join(
    f'''  <url>
    <loc>{SITE}/{"" if n == "index.html" else n}</loc>
    <lastmod>{today_iso}</lastmod>
    <priority>{priority.get(n, "0.7")}</priority>
  </url>''' for n in pages)
(out / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
''')
(out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

svc = "\n".join(f"- {d}: {m}, {t}" for _, d, m, t in SERVICES)
(out / "llms.txt").write_text(f"""# {NAME} ({SHORT})

> A prophetic and apostolic church in Adzen (Adjen-Kotoku), Ga West, Greater Accra, Ghana, led by Apostle Victor Annan.

## Key facts
- Name: {NAME} ({SHORT})
- Leader: Apostle Victor Annan (also styled Bishop Victor Annan); Rev. Mrs Natalie Annan ministers alongside him
- Address: Last stop, Adjen-Kotoku, next to Pick N Nikki School, Adzen, Ga West, Greater Accra, Ghana
- GhanaPostGPS digital address: {GPS}
- Coordinates: {LAT}, {LNG}
- Phone: 059 660 9093, 020 171 3589 (WhatsApp: 059 660 9093)
- Website: {SITE}/

## Service times (Ghana time, GMT)
{svc}

## Vision
To raise an indigenous and self-supporting church, and to demonstrate the love of God in our generation.

## Mission
1. To preach the undiluted Word of God.
2. Spiritual growth, numerical growth and financial growth.
3. Equipping the saints of Christ (Ephesians 4:11-13).

## Focus
The sub-communities around the church, the youth and the children, training them with vocational skills.

## Goals
1. To reach the unreached.
2. To help the less privileged.
3. To help the aged.

## Upcoming event
- At His Feet, worship all night: Friday 4 December 2026 from 8:00 PM at the church premises.

## Pages
{chr(10).join(f"- [{CRUMB.get(n, 'Home')}]({SITE}/{'' if n == 'index.html' else n})" for n in pages)}
""")

# Link-preview cards: one per page, rendered by og/make_cards.js
import json
OG_CARDS = {
    "index": ("Faith Demonstration Ministries International", "A prophetic and apostolic church in Adjen-Kotoku, Accra", "photos/worship-team.jpg", "50% 40%"),
    "about": ("About the church", "To raise an indigenous and self-supporting church, and to demonstrate the love of God in our generation", "photos/church-family.jpg", "50% 35%"),
    "leaders": ("Leaders", "Apostle Victor Annan, Rev. Mrs Natalie Annan and the ministry team", "photos/consecration.jpg", "50% 25%"),
    "ministries": ("Ministries", "Worship, prayer, youth, children, and outreach and welfare", "photos/youth-night.jpg", "50% 40%"),
    "sermons": ("Sermons", "Divine Service on Sundays and Study His Word on Tuesdays", "photos/hands-raised.jpg", "50% 40%"),
    "events": ("At His Feet: worship all night", "Friday 4 December 2026, from 8:00 PM", "at-his-feet-flyer.jpg", "50% 22%"),
    "announcements": ("Announcements", "News for the FDMI church family", "photos/sunday-service.jpg", "40% 50%"),
    "visit": ("Plan your visit", "Service times, directions and what to expect", "photos/white-service-1.jpg", "50% 45%"),
    "gallery": ("Gallery", "Photos and video from life at FDMI", "photos/family-celebration.jpg", "50% 30%"),
}
(out / "og" ).mkdir(exist_ok=True)
(out / "og" / "cards.json").write_text(json.dumps(
    [{"name": k, "title": t, "sub": sub, "img": img, "pos": pos} for k, (t, sub, img, pos) in OG_CARDS.items()], indent=1))
print("wrote sitemap.xml, robots.txt, llms.txt, og/cards.json")
