#!/usr/bin/env python3
"""Inject OGP/Twitter-card meta + Schema.org JSON-LD into each page's <head>."""
import json, os, re
from PIL import Image

SITE = "https://www.captainsflathotel.com.au"
NAME = "Captains Flat Hotel"
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pub")

ADDR = {
    "@type": "PostalAddress",
    "streetAddress": "51 Foxlow Street",
    "addressLocality": "Captains Flat",
    "addressRegion": "NSW",
    "postalCode": "2623",
    "addressCountry": "AU",
}
GEO = {"@type": "GeoCoordinates", "latitude": -35.59213, "longitude": 149.445003}
SOCIALS = [
    "https://www.facebook.com/people/Captains-Flat-Hotel/100083311546250/",
    "https://www.instagram.com/captainsflat.hotel/",
    "https://www.tiktok.com/@captains.flat.hotel",
]
PHONE = "+61-2-6236-6069"
EMAIL = "captainsflathub@gmail.com"

HOURS_BAR = [
    ("Wednesday", "11:00", "19:30"), ("Thursday", "11:00", "19:30"),
    ("Friday", "11:00", "20:00"), ("Saturday", "11:00", "20:00"),
    ("Sunday", "11:00", "14:30"),
]
HOURS_KITCHEN_LUNCH = [
    ("Wednesday", "12:00", "14:00"), ("Thursday", "12:00", "14:00"),
    ("Friday", "12:00", "14:00"), ("Saturday", "12:00", "15:00"),
    ("Sunday", "12:00", "14:30"),
]
HOURS_KITCHEN_DINNER = [
    ("Wednesday", "17:30", "19:30"), ("Thursday", "17:30", "19:30"),
    ("Friday", "17:30", "20:00"), ("Saturday", "17:30", "20:00"),
]

def oh(specs):
    return [{"@type": "OpeningHoursSpecification", "dayOfWeek": d,
             "opens": o, "closes": c} for d, o, c in specs]

def img_url(p): return f"{SITE}/images/{p}"
def page_url(f): return SITE + ("/" if f == "index.html" else f"/{f}")

def offer(price):
    return {"@type": "Offer", "price": price, "priceCurrency": "AUD"}

# ---------- shared entity nodes ----------

def hotel_node():
    return {
        "@type": "Hotel",
        "@id": f"{SITE}/#hotel",
        "name": NAME,
        "alternateName": "The Flat",
        "slogan": "Home of the Legendary Floating Beer Glass",
        "description": "Heritage Art Deco country pub in Captains Flat, NSW, serving cold beer, quality pub meals and cosy accommodation since 1938. Home of the 1938 whisky bar and the legendary floating beer glass.",
        "url": SITE,
        "telephone": PHONE,
        "email": EMAIL,
        "address": ADDR,
        "geo": GEO,
        "image": [img_url("hero-front.jpg"), img_url("whisky-bar.jpg"),
                  img_url("floating-glass.jpg")],
        "priceRange": "$$",
        "foundingDate": "1938",
        "currenciesAccepted": "AUD",
        "paymentAccepted": "Cash, Credit Card, EFTPOS",
        "sameAs": SOCIALS,
        "openingHoursSpecification": oh(HOURS_BAR),
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Wood fireplace", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "1938 whisky bar", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Continental breakfast available", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Balcony access (some rooms)", "value": True},
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "email": EMAIL,
            "contactType": "reservations",
            "availableLanguage": "English",
        },
        "containsPlace": [
            {"@id": f"{SITE}/#restaurant"},
            {"@id": f"{SITE}/#bar1938"},
            {"@id": f"{SITE}/#room-single"},
            {"@id": f"{SITE}/#room-twin"},
            {"@id": f"{SITE}/#room-queen"},
        ],
        "hasMap": "https://maps.google.com/?q=Captains+Flat+Hotel,+51+Foxlow+St,+Captains+Flat+NSW+2623",
    }

def restaurant_node():
    return {
        "@type": "Restaurant",
        "@id": f"{SITE}/#restaurant",
        "name": f"{NAME} Restaurant",
        "description": "Classic country pub meals including steaks, schnitzels, parmigiana, plus vegetarian and kids options.",
        "url": f"{SITE}/menu.html",
        "telephone": PHONE,
        "servesCuisine": ["Australian", "Pub Food"],
        "priceRange": "$$",
        "acceptsReservations": "True",
        "menu": f"{SITE}/menu.html",
        "address": ADDR,
        "geo": GEO,
        "openingHoursSpecification": oh(HOURS_KITCHEN_LUNCH + HOURS_KITCHEN_DINNER),
    }

def bar1938_node():
    return {
        "@type": "BarOrPub",
        "@id": f"{SITE}/#bar1938",
        "name": "1938 — The Whisky Bar",
        "description": "An intimate whisky bar inside the Captains Flat Hotel, named for the year the Art Deco building opened. Australian and international whiskies, premium spirits, local wines and classic cocktails.",
        "url": f"{SITE}/1938.html",
        "telephone": PHONE,
        "address": ADDR,
        "geo": GEO,
        "image": img_url("whisky-bar.jpg"),
        "servesCuisine": "Whisky, Spirits, Wine, Cocktails",
    }

def room_nodes():
    return [
        {
            "@type": "HotelRoom", "@id": f"{SITE}/#room-single",
            "name": "Single Room",
            "description": "Original 1937 cast iron single bed, solid oak Art Deco wardrobe, woollen blanket and electric blanket.",
            "image": img_url("room-single.jpg"),
            "bed": {"@type": "BedDetails", "typeOfBed": "Single", "numberOfBeds": 1},
            "occupancy": {"@type": "QuantitativeValue", "maxValue": 1, "unitText": "guest"},
            "containedInPlace": {"@id": f"{SITE}/#hotel"},
            "offers": offer("90.00"),
        },
        {
            "@type": "HotelRoom", "@id": f"{SITE}/#room-twin",
            "name": "Twin Single Room",
            "description": "Two original 1937 cast iron single beds, solid oak custom-made wardrobe and electric blankets.",
            "image": img_url("room-twin.jpg"),
            "bed": {"@type": "BedDetails", "typeOfBed": "Single", "numberOfBeds": 2},
            "occupancy": {"@type": "QuantitativeValue", "maxValue": 2, "unitText": "guests"},
            "containedInPlace": {"@id": f"{SITE}/#hotel"},
            "offers": offer("110.00"),
        },
        {
            "@type": "HotelRoom", "@id": f"{SITE}/#room-queen",
            "name": "Double & Queen Rooms",
            "description": "One double or queen bed; some rooms with balcony access.",
            "image": img_url("room-queen.jpg"),
            "bed": {"@type": "BedDetails", "typeOfBed": "Queen", "numberOfBeds": 1},
            "occupancy": {"@type": "QuantitativeValue", "maxValue": 2, "unitText": "guests"},
            "containedInPlace": {"@id": f"{SITE}/#hotel"},
            "offers": offer("110.00"),
        },
    ]

def website_node():
    return {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": SITE,
        "name": NAME,
        "publisher": {"@id": f"{SITE}/#hotel"},
        "inLanguage": "en-AU",
    }

def webpage_node(fname, title, desc, og_img, ptype="WebPage", about="#hotel"):
    return {
        "@type": ptype,
        "@id": f"{page_url(fname)}#webpage",
        "url": page_url(fname),
        "name": title,
        "description": desc,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": f"{SITE}/{about}"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": img_url(og_img)},
        "inLanguage": "en-AU",
    }

def breadcrumb(fname, label):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    if fname != "index.html":
        items.append({"@type": "ListItem", "position": 2,
                      "name": label, "item": page_url(fname)})
    return {"@type": "BreadcrumbList", "@id": f"{page_url(fname)}#breadcrumb",
            "itemListElement": items}

# ---------- page-specific schema ----------

def menu_item(name, price, desc=None):
    it = {"@type": "MenuItem", "name": name, "offers": offer(f"{price:.2f}")}
    if desc: it["description"] = desc
    return it

def menu_node():
    def section(name, items):
        return {"@type": "MenuSection", "name": name, "hasMenuItem": items}
    return {
        "@type": "Menu", "@id": f"{SITE}/menu.html#menu",
        "name": f"{NAME} Menu",
        "hasMenuSection": [
            section("Starters", [
                menu_item("Garlic Bread", 9.50),
                menu_item("Chips & Gravy", 11),
                menu_item("Wedges", 14, "Sweet chilli & sour cream"),
                menu_item("Salt & Pepper Squid", 15, "Szechuan seasoning & sriracha lime mayo"),
                menu_item("Half Kilo Wings", 17, "Southern fried w/ chipotle mayo, Buffalo w/ garlic aioli, or honey soy"),
                menu_item("Glazed Pork Belly Bites", 18, "Apple slaw"),
            ]),
            section("The Classics", [
                menu_item("Beef Lasagne", 24, "With salad"),
                menu_item("Fish & Chips", 27, "Hake, chips & salad"),
                menu_item("Pot Pie", 24, "Mash & mushy peas"),
                menu_item("Chicken Schnitzel", 29, "House panko crumbed, 2 sides & sauce"),
                menu_item("Chicken Parmigiana", 35, "Ham, cheese, Neapolitan sauce, 2 sides"),
                menu_item("Vegetarian Schnitzel", 26, "2 sides & sauce"),
                menu_item("Porterhouse Steak ~300gm", 44, "Gluten free, 2 sides & sauce"),
                menu_item("Lamb Shanks", 27, "Mash & broccolini (1 shank $27, 2 shanks $34)"),
            ]),
            section("For the Kids", [
                menu_item("Chicken Nuggets", 10, "Small $10 / large $14"),
                menu_item("Fish & Chips", 14),
                menu_item("Cheese Burger", 14),
                menu_item("Kids Ice Cream", 4, "Choc, caramel or strawberry topping"),
            ]),
            section("Dessert", [
                menu_item("Churros", 12),
                menu_item("Chocolate Mud Cake", 12, "Served with chocolate ice cream"),
                menu_item("Apple Crumble Tartlet", 12, "Vanilla ice cream"),
                menu_item("Ice Cream Cup or Waffle Cone", 4, "Per scoop — chocolate, vanilla, hokey pokey, rainbow"),
            ]),
        ],
    }

def taps_node():
    beers = [
        ("Travla", "Full-strength Australian lager, smooth light body, crisp refreshing finish. Australian pale malt, Cluster & Melba hops.", "4.2% ABV, low carb", "tap-travla.png"),
        ("Carlton Draught", "Traditional full-strength lager, good malt character, smooth full-bodied flavour, slightly dry finish.", "4.6% ABV", "tap-carlton-draught.jpg"),
        ("Reschs Draught", "Iconic NSW brew — a fruity, golden lager.", "4.5% ABV", "tap-reschs.jpg"),
        ("Great Northern Super Crisp", "Clean crisp lager brewed with all Australian ingredients, mild fruitiness and smooth bitterness.", "3.5% ABV, ultra low carb", "tap-great-northern.jpg"),
        ("Asahi", "Light golden, fruity aroma, subtle bitterness, refreshingly clean and crisp finish.", "4.2% ABV", "tap-asahi.jpg"),
        ("Carlton Dry", "Signature ultra smooth refreshment — a little fruity, low in bitterness.", "3.5% ABV", "tap-carlton-dry.jpg"),
        ("Victoria Bitter", "Brewed since 1854 — full flavoured, full strength, thirst quenching.", "Full strength", "tap-vb.png"),
        ("Hard Rated", "Original lemon flavour made with crushed lemons.", "4.5% ABV", "tap-hard-rated.jpg"),
    ]
    return {
        "@type": "Menu", "@id": f"{SITE}/on-tap.html#menu",
        "name": "Beers on Tap",
        "hasMenuSection": [{
            "@type": "MenuSection", "name": "Beers on Tap",
            "hasMenuItem": [
                {"@type": "MenuItem", "name": n,
                 "description": f"{d} ({abv})",
                 "image": img_url(img)} for n, d, abv, img in beers
            ],
        }],
    }

def merch_node():
    products = [
        ("Captains Flat Hotel Hoodie", "Navy hoodie with gold CFH Est. 1938 roundel. Sizes SM–4XL.", "75.00", "merch-hoodie-front.jpg"),
        ('"I Stuck It at The Flat" Tee', "Bloody Legend Status Achieved — earn $5 off by floating your glass.", "30.00", "merch-stuck-shirt.jpg"),
        ("Long Sleeve Tee", "Captains Flat Hotel long sleeve t-shirt. Sizes SM–2XL.", "50.00", "merch-longsleeve.jpg"),
        ("Classic Truckers Hat", "Available in pink, navy and tan.", "35.00", "merch-hat-navy.jpg"),
        ("CFH Beanie", "Warm knit beanie with CFH Est. 1938 patch.", "30.00", "merch-beanie.jpg"),
        ("Stubby Holder", "Captains Flat Hotel stubby holder.", "10.00", "merch-stubby.jpg"),
        ("Bumper Sticker", "Captains Flat Hotel bumper sticker.", "5.00", "badge-cfh.jpg"),
    ]
    return {
        "@type": "ItemList", "@id": f"{SITE}/merch.html#items",
        "name": f"{NAME} Merchandise",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "item": {"@type": "Product", "name": n, "description": d,
                      "image": img_url(im), "brand": {"@type": "Brand", "name": NAME},
                      "offers": {**offer(p), "availability": "https://schema.org/InStock",
                                 "itemCondition": "https://schema.org/NewCondition"}}}
            for i, (n, d, p, im) in enumerate(products)],
    }

def gallery_node():
    groups = [
        ("bar", 5, "1938 — The Whisky Bar, first birthday celebrations"),
        ("film", 10, "The Narrow Road to the Deep North — behind the scenes"),
        ("finke", 3, "Mick Pearce — Tatts Finke Desert Race 2025"),
        ("anzac", 1, "ANZAC Day 2025"),
        ("ausday", 1, "Australia Day 2025"),
    ]
    imgs = []
    for prefix, count, caption in groups:
        for i in range(1, count + 1):
            imgs.append({"@type": "ImageObject",
                         "contentUrl": img_url(f"gallery/{prefix}-{i:02d}.jpg"),
                         "name": caption})
    return {"@type": "ImageGallery", "@id": f"{SITE}/gallery.html#gallery",
            "name": f"{NAME} Gallery", "image": imgs}

def attractions_node():
    sights = [
        ("Captain's Flat Lookout", "Panoramic views over the town and the surrounding Jingera Mountains — great for photography and getting your bearings."),
        ("Welcome to Captains Flat Sign", "The popular, quirky landmark greeting visitors on arrival — a favourite photo stop."),
        ("Wilkins Park", "Scenic recreation ground beside the Molonglo River, proclaimed 1893. Historic water trough and picnic facilities."),
        ("Captains Flat War Memorial", "Honours local history and those who served, in the centre of town near Wilkins Park."),
        ("Captains Flat Dam", "A peaceful, secluded spot for anglers, surrounded by bushland and unique geological formations."),
        ("Tallaganda State Forest", "Rugged forest surrounding the area — popular for 4WD exploration, bushwalking and camping."),
    ]
    return {
        "@type": "ItemList", "@id": f"{SITE}/explore.html#attractions",
        "name": "Local Attractions — Captains Flat NSW",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "item": {"@type": "TouristAttraction", "name": n, "description": d,
                      "address": ADDR}}
            for i, (n, d) in enumerate(sights)],
    }

def campground_node():
    return {
        "@type": "Campground", "@id": f"{SITE}/camp.html#campground",
        "name": "Wilkins Memorial Park Camping Area",
        "alternateName": "Wilkins Park",
        "description": "Donation-based camping beside the Molonglo River in Captains Flat, managed by a local community committee on behalf of Queanbeyan-Palerang Regional Council. Hot showers, toilets and drinking water on site; donations via the mailbox at the Men's Shed opposite.",
        "address": ADDR,
        "priceRange": "Donation",
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Hot showers", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Toilets", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Drinking water", "value": True},
        ],
        "isAccessibleForFree": True,
        "paymentAccepted": "Donation",
    }

# ---------- per-page config ----------

PAGES = {
    "index.html": {
        "title": "Captains Flat Hotel — Est. 1938 | Country Pub, Whisky Bar & Accommodation",
        "desc": "Heritage Art Deco country pub in Captains Flat, NSW. Cold beer, quality pub meals, cosy rooms and the 1938 whisky bar. Home of the legendary floating beer glass.",
        "og": "hero-front.jpg", "crumb": "Home", "ptype": "WebPage",
        "extra": [],
    },
    "menu.html": {
        "title": "Menu — Captains Flat Hotel",
        "desc": "Pub classics, starters, kids meals and desserts at the Captains Flat Hotel. Schnitzel, parmi, steaks, wings and more.",
        "og": "offer-meal.jpg", "crumb": "Menu", "ptype": "WebPage",
        "about": "#restaurant", "extra": [menu_node],
    },
    "on-tap.html": {
        "title": "Beers on Tap — Captains Flat Hotel",
        "desc": "Cold draught beer at the Captains Flat Hotel — eight taps pouring classic Australian lagers and more.",
        "og": "fireplace.jpg", "crumb": "Beers on Tap", "ptype": "WebPage",
        "extra": [taps_node],
    },
    "1938.html": {
        "title": "1938 — The Whisky Bar | Captains Flat Hotel",
        "desc": "1938 is the Captains Flat Hotel's intimate whisky bar — Australian and international whiskies, premium spirits, local wines and classic cocktails in an Art Deco setting.",
        "og": "whisky-bar.jpg", "crumb": "1938 Whisky Bar", "ptype": "AboutPage",
        "about": "#bar1938", "extra": [],
    },
    "stay.html": {
        "title": "Stay — Accommodation | Captains Flat Hotel",
        "desc": "Cosy heritage rooms at the Captains Flat Hotel — single $90, twin $110, double & queen $110. Call (02) 6236 6069 to book.",
        "og": "offer-room.jpg", "crumb": "Accommodation", "ptype": "WebPage",
        "extra": [room_nodes],
    },
    "gallery.html": {
        "title": "Gallery — Captains Flat Hotel",
        "desc": "Photos from the Captains Flat Hotel — the 1938 whisky bar, movie shoots, race days and community events.",
        "og": "gallery/bar-01.jpg", "crumb": "Gallery", "ptype": "CollectionPage",
        "extra": [gallery_node],
    },
    "merch.html": {
        "title": "Merchandise — Captains Flat Hotel",
        "desc": "Captains Flat Hotel merch — hoodies, tees, trucker hats, beanies, stubby holders and bumper stickers. Available at the bar.",
        "og": "merch-hero.jpg", "crumb": "Merchandise", "ptype": "CollectionPage",
        "extra": [merch_node],
    },
    "camp.html": {
        "title": "Camp at The Flat — Caravans, Campers & Backpackers | Captains Flat Hotel",
        "desc": "Donation-based camping at Wilkins Memorial Park, Captains Flat — or park the van and take a hotel room from $90. Hot showers, toilets and drinking water beside the Molonglo River.",
        "og": "hero-front.jpg", "crumb": "Camping", "ptype": "WebPage",
        "extra": [campground_node],
    },
    "explore.html": {
        "title": "Explore — Local Attractions | Captains Flat Hotel",
        "desc": "Things to see and do around Captains Flat NSW — about an hour from Canberra. The lookout, Wilkins Park on the Molonglo River, the war memorial, fishing at the dam and Tallaganda State Forest.",
        "og": "gallery/ausday-01.jpg", "crumb": "Local Attractions", "ptype": "WebPage",
        "extra": [attractions_node],
    },
    "history.html": {
        "title": "The History of Captains Flat — Boom, Bust & the Pub | Captains Flat Hotel",
        "desc": "From a bull named Captain to a gold rush, two mining booms and a railway — the story of Captains Flat, and the 1938 Art Deco pub that has been its heart ever since.",
        "og": "hero-front.jpg", "crumb": "Town History", "ptype": "AboutPage",
        "extra": [],
    },
    "events.html": {
        "title": "Events & Weddings — Host It at The Flat | Captains Flat Hotel",
        "desc": "Hold your wedding, party, club run or gathering in Captains Flat — a whole heritage village with riverside parkland, camping, a community hall and a 1938 pub as its clubhouse.",
        "og": "hero-front.jpg", "crumb": "Events", "ptype": "WebPage",
        "extra": [],
    },
    "play.html": {
        "title": "Play The Flat — Gigs for Touring Artists | Captains Flat Hotel",
        "desc": "Touring artists and musos — bring a gig to the Captains Flat Hotel, a 1938 Art Deco pub where the whole town shows up. Donation camping or rooms from $90 for the band.",
        "og": "gallery/bar-01.jpg", "crumb": "Play a Gig", "ptype": "WebPage",
        "extra": [],
    },
    "visit.html": {
        "title": "Visit Us — Opening Hours & Contact | Captains Flat Hotel",
        "desc": "Opening hours, location and contact details for the Captains Flat Hotel — 51 Foxlow St, Captains Flat NSW 2623. Call (02) 6236 6069.",
        "og": "hero-front.jpg", "crumb": "Visit", "ptype": "ContactPage",
        "extra": [],
    },
}


def build(fname, cfg):
    url = page_url(fname)
    img = img_url(cfg["og"])
    with Image.open(os.path.join(PUB, "images", cfg["og"])) as im:
        w, h = im.size

    meta = f'''<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_AU">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{cfg['title']}">
<meta property="og:description" content="{cfg['desc']}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta property="og:image:alt" content="{NAME} — {cfg['crumb']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{cfg['title']}">
<meta name="twitter:description" content="{cfg['desc']}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#131110">'''

    graph = [
        website_node(),
        hotel_node(),
        restaurant_node(),
        bar1938_node(),
        webpage_node(fname, cfg["title"], cfg["desc"], cfg["og"],
                     cfg["ptype"], cfg.get("about", "#hotel")),
        breadcrumb(fname, cfg["crumb"]),
    ]
    for fn in cfg["extra"]:
        extra = fn() if callable(fn) else fn
        graph.extend(extra if isinstance(extra, list) else [extra])

    ld = '<script type="application/ld+json">\n' + \
         json.dumps({"@context": "https://schema.org", "@graph": graph},
                    indent=2, ensure_ascii=False) + "\n</script>"
    return meta + "\n" + ld


for fname, cfg in PAGES.items():
    path = os.path.join(PUB, fname)
    doc = open(path, encoding="utf-8").read()
    if "og:site_name" in doc:
        print(f"{fname}: already done"); continue
    marker = '<link rel="icon"'
    idx = doc.index(marker)
    doc = doc[:idx] + build(fname, cfg) + "\n" + doc[idx:]
    open(path, "w", encoding="utf-8").write(doc)
    print(f"{fname}: injected {doc.count('application/ld+json')} json-ld block(s)")
