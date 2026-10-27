"""Generate the per-app privacy policy pages.

usage: python3 tools/build_privacy.py   (run from the repository root)

Each policy is written to <slug>-privacy-policy.html, the same path the old
site used, so links in existing store listings keep working.
"""
import html

UPDATED = "October 26, 2026"
CONTACT = "support@jamesmorrisstudios.us"
GOOGLE_PRIVACY = "https://policies.google.com/privacy"
OSM_PRIVACY = "https://osmfoundation.org/wiki/Privacy_Policy"

PLAY_GAMES = (
    "Google Play Games",
    f"""<p>If you are signed in to Google Play Games on your device, the app unlocks your
achievements and submits your scores to its leaderboards. That information is sent to and
stored by Google as part of your Play Games profile, and is handled under the
<a href="{GOOGLE_PRIVACY}">Google Privacy Policy</a>. You can manage your Play Games profile
and visibility in the Google Play Games settings.</p>""",
)

SHARING = (
    "Sharing",
    """<p>The share button opens Android's share sheet. Whatever you choose to share is sent
with the app you pick, under that app's own policy.</p>""",
)

APPS = [
    {
        "slug": "randomly-remindme",
        "name": "Randomly RemindMe",
        "stored": """<p>Your reminders, their messages, images and logs, and your settings are
stored on your device. Backups and exports are saved only where you choose to save them.</p>""",
        "sections": [
            ("Location", """<p>Location-based reminders use your device's location to check
whether you are in a reminder's area. This happens on your device and your location is not
sent anywhere. The app only uses location if you set up a location-based reminder and grant
the location permission.</p>"""),
            ("Maps", f"""<p>When you pick a location for a reminder, the map is loaded from
OpenStreetMap's tile servers. Those servers receive the normal information of a web request,
such as your IP address and which map area is shown, and handle it under the
<a href="{OSM_PRIVACY}">OpenStreetMap Foundation Privacy Policy</a>.</p>"""),
            ("RSS feeds and reminder packs", """<p>If a reminder uses an RSS feed for its
messages, the app downloads that feed from the address you entered. If you open a link to a
reminder pack, the app downloads that file. No information about you is sent with these
requests beyond what any web request includes.</p>"""),
            ("Automation apps", """<p>If you set a reminder to send an Android intent to an
automation app, the app sends only the intent you configured, to the app you chose.</p>"""),
        ],
        "permissions": [
            ("Notifications, alarms and vibration", "to deliver reminders at their scheduled times"),
            ("Run at startup", "to reschedule reminders after the device restarts"),
            ("Location", "only for location-based reminders"),
            ("Internet and network state", "for maps, RSS feeds and reminder packs"),
            ("Storage", "for images, backups and exports you choose"),
        ],
    },
    {
        "slug": "match-the-block",
        "name": "Match the Block",
        "stored": """<p>Your game in progress, high scores, statistics and settings are stored
on your device.</p>""",
        "sections": [PLAY_GAMES, SHARING],
        "permissions": [],
    },
    {
        "slug": "one-and-up",
        "name": "One &amp; Up",
        "stored": """<p>Your game in progress, high scores, statistics and settings are stored
on your device.</p>""",
        "sections": [PLAY_GAMES, SHARING],
        "permissions": [],
    },
    {
        "slug": "bandit-five",
        "name": "BandIt Five",
        "stored": """<p>Your game in progress, finished games and statistics, and settings are
stored on your device.</p>""",
        "sections": [PLAY_GAMES, SHARING],
        "permissions": [],
    },
]

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="icon" href="/favicon.png">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <header>
    <a class="home" href="/">James Morris Studios</a>
  </header>

  <main>
    <h1>Privacy Policy for {name}</h1>
    <p class="muted">Last updated: {updated}</p>

    <p>This policy explains how {name}, an Android app by James Morris Studios, handles your
information.</p>

    <h2>Summary</h2>
    <p>James Morris Studios does not collect, store, sell or share any personal information
from {name}. The app has no ads, analytics or tracking.</p>

    <h2>Information stored on your device</h2>
    {stored}
    <p>This information is removed when you uninstall the app. If Android backup is turned
on for your device, Android may include the app's data in your device backup in your
Google account and restore it when you reinstall the app or set up a new device. That
backup is handled by Google under the
<a href="{google_privacy}">Google Privacy Policy</a>, and you can turn it off in your
device's backup settings. James Morris Studios never receives this data.</p>
{sections}
    <h2>Permissions</h2>
{permissions}

    <h2>Children</h2>
    <p>Because the app does not collect personal information, it does not knowingly collect
information from children.</p>

    <h2>Changes to this policy</h2>
    <p>If this policy changes, the updated version will be posted on this page with a new
date.</p>

    <h2>Contact</h2>
    <p>Questions about this policy can be sent to
<a href="mailto:{contact}">{contact}</a>.</p>
  </main>

  <footer>
    <a href="/">James Morris Studios</a>
  </footer>
</body>
</html>
"""


def main():
    for app in APPS:
        sections = "".join(f"\n    <h2>{title}</h2>\n    {body}\n" for title, body in app["sections"])
        if app["permissions"]:
            items = "\n".join(
                f"      <li><strong>{html.escape(name)}</strong>: {html.escape(why)}</li>"
                for name, why in app["permissions"]
            )
            permissions = f"    <ul>\n{items}\n    </ul>"
        else:
            permissions = "    <p>The app does not request any device permissions.</p>"
        page = PAGE.format(
            title=f"Privacy Policy - {app['name']}",
            name=app["name"],
            updated=app.get("updated", UPDATED),
            stored=app["stored"],
            sections=sections,
            permissions=permissions,
            contact=CONTACT,
            google_privacy=GOOGLE_PRIVACY,
        )
        path = f"{app['slug']}-privacy-policy.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print("wrote", path)


if __name__ == "__main__":
    main()
