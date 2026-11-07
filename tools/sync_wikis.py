"""Publish site-derived Markdown snapshots to the three Softmax wikis."""

import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, urljoin

from bs4 import BeautifulSoup, Comment, NavigableString
import httpx

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://softmax-universe.github.io/polyworld-buff/"
SERVER = "https://softmax.com/api"
MEDIA = "https://softmax-public.s3.amazonaws.com/"
GAMES = [
  ("GOTA", "Gods of the Arena", "gods-of-the-arena"),
  ("LvD", "Light vs Dark", "light-vs-dark"),
  ("CTA", "Call to Adventure", "call-to-adventure"),
]


def saveJson(file, value):
  """Save public synchronization metadata atomically."""
  temporary = file.with_suffix(".tmp")
  temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
  temporary.replace(file)


def digest(value):
  """Identify exact content without storing credentials."""
  return hashlib.sha256(value).hexdigest()


def table(headers, rows):
  """Render a Markdown table with escaped cell separators."""
  lines = [headers, ["---"] * len(headers), *rows]
  return "\n".join(
    "| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |"
    for row in lines
  ) + "\n\n"


def markdown(node, page, images):
  """Convert the guide's semantic content into wiki-safe Markdown."""
  if isinstance(node, Comment):
    return ""
  if isinstance(node, NavigableString):
    return re.sub(r"\s+", " ", str(node))
  if node.name in ("script", "style", "svg", "button", "nav"):
    return ""
  if node.name == "img":
    label = node.get("alt", "")
    if not label:
      return ""
    file = (page.parent / node["src"]).resolve()
    key = digest(file.read_bytes())
    if key not in images:
      return label
    return f"\n\n![{label}]({images[key]})\n\n"
  if node.name == "table":
    rows = [
      [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
      for row in node.find_all("tr")
    ]
    return "\n\n" + table(rows[0], rows[1:])
  if node.name == "dl":
    rows = [
      [
        term.get_text(" ", strip=True),
        term.find_next_sibling("dd").get_text(" ", strip=True),
      ]
      for term in node.find_all("dt")
    ]
    return "\n\n" + table(["Property", "Value"], rows)
  classes = set(node.get("class", []))
  if classes & {"facts", "stats"}:
    rows = [
      [item.find("span").get_text(" ", strip=True),
       item.find("b").get_text(" ", strip=True)]
      for item in node.select(".fact, .stat")
    ]
    return "\n\n" + table(["Stat", "Value"], rows)
  if "lanes" in classes:
    rows = [
      [item.find("b").get_text(" ", strip=True),
       item.select_one(".muted").get_text(" ", strip=True)]
      for item in node.select(".chip")
    ]
    return "\n\n" + table(["Reference", "Details"], rows)
  if "abilities" in classes and page.parent.name == "CTA":
    rows = [
      [ability.select_one(".key").get_text(" ", strip=True),
       ability.find("h4").get_text(" ", strip=True),
       " · ".join(tag.get_text(" ", strip=True)
                  for tag in ability.select(".meta .tag"))]
      for ability in node.select(".ability")
    ]
    return "\n\n" + table(["Key", "Ability", "Details"], rows)
  content = "".join(markdown(child, page, images) for child in node.children)
  if set(node.get("class", [])) & {"stat", "fact", "chip"}:
    return "\n- " + re.sub(r"\s+", " ", content).strip() + "\n"
  if node.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
    return "\n\n" + "#" * int(node.name[1]) + " " + content.strip() + "\n\n"
  if node.name in ("b", "strong"):
    return "**" + content.strip() + "** "
  if node.name in ("em", "i"):
    return "*" + content.strip() + "* " if content.strip() else ""
  if node.name == "code":
    return "`" + content.strip() + "`"
  if node.name == "a":
    url = urljoin(SITE + page.relative_to(ROOT).as_posix(), node["href"])
    return f"[{content.strip()}]({url})"
  if node.name == "li":
    return "\n- " + content.strip()
  if node.name == "br":
    return "\n"
  if node.name == "span":
    return " " + content.strip() + " "
  if node.name in ("div", "p", "section", "article", "ul", "ol", "summary"):
    return "\n\n" + content.strip() + "\n\n" if content.strip() else ""
  return content


def guide(folder, images):
  """Export a guide while leaving browser-only controls on the site."""
  page = ROOT / folder / "index.html"
  soup = BeautifulSoup(page.read_text(), "html.parser")
  content = soup.find("main")
  for element in content.select(
    ".standings-callout, .balance-callout, .hero-balance, "
    "[aria-label='Interactive charge timing example']"
  ):
    element.decompose()
  text = markdown(soup.find("img"), page, images) + markdown(content, page, images)
  text = "\n".join(line.strip() for line in text.splitlines())
  return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def heroStats():
  """Export dated aggregate hero statistics and their interpretation."""
  soup = BeautifulSoup((ROOT / "GOTA/heros/index.html").read_text(), "html.parser")
  summary = json.loads(soup.find("script", id="report-data").string)["summary"]
  text = (
    f"Analysis window: **{summary['start']} to {summary['end']}**.\n\n"
    f"{summary['verified_games']} verified games; "
    f"{summary['hero_appearances']} hero appearances. This is a dated snapshot.\n\n"
    "Fixed faction lineups share outcomes. Win rate measures faction results, "
    "not a hero's causal strength. Draws count as non-wins. "
    "Compare game versions separately.\n\n"
  )
  for scope in [summary, *summary["versions"]]:
    label = "All versions" if scope is summary else scope["version"]
    text += f"## {label} ({scope['games']} games)\n\n"
    rows = []
    for hero in scope["heroes"]:
      rows.append([
        hero["hero"], f"{hero['win_rate']:.1%}", f"{hero['avg_level']:.2f}",
        f"{hero['avg_kills']:.2f} / {hero['avg_deaths']:.2f} / {hero['avg_assists']:.2f}",
        f"{hero['xp_per_minute']:.1f}", f"{hero['gold_per_minute']:.1f}",
      ])
    text += table(["Hero", "Win rate", "Level", "K / D / A", "XP/min", "Gold/min"], rows)
  text += "## Methodology\n\n"
  for paragraph in soup.select(".methods p"):
    text += paragraph.get_text(" ", strip=True) + "\n\n"
  return text


def standings():
  """Export all six standings tables without copying replay payloads."""
  soup = BeautifulSoup((ROOT / "GOTA/standings/index.html").read_text(), "html.parser")
  data = json.loads(soup.find("script", id="report-data").string)
  text = (
    f"Tournament: **{data['run']}**. Updated **{data['updated']}**.\n\n"
    f"Game version **{data['release']['version']}**. "
    f"{data['completed']}/{data['target']} games completed; "
    f"{data['included']} included; {data['failed']} failed. "
    "This is a published tournament snapshot, not the live platform leaderboard.\n\n"
  )
  for panel in data["panels"]:
    text += f"## {panel['format'].title()} teams: {panel['title']}\n\n"
    rows = []
    for row in panel["rows"]:
      value = f"{row['value']:.1%}" if panel["ladder"] == "wins" else f"{row['value']:.2f}"
      rows.append([row["rank"], row["name"], row["version"], row["appearances"], value])
    text += table(["Rank", "Player", "Policy", "Appearances", panel["title"]], rows)
  players = soup.find("table", id="player-stats")
  if players:
    text += "## Player statistics\n\nBoth formats, per-player averages.\n\n"
    headers = [
      cell.get_text(" ", strip=True).replace("↕", "").strip()
      for cell in players.select("thead th")
    ]
    rows = [
      [cell.get_text(" · ", strip=True) for cell in row.find_all(["th", "td"])]
      for row in players.select("tbody tr")
    ]
    text += table(headers, rows)
    for paragraph in players.find_parent("section").find_all("p"):
      text += paragraph.get_text(" ", strip=True).replace(
        " Click a column heading to sort.", ""
      ) + "\n\n"
  footer = soup.find("footer")
  if footer:
    text += "## How to read the standings\n\n" + footer.get_text(" ", strip=True) + "\n"
  return text


def main():
  """Generate local snapshots or explicitly publish them with revision checks."""
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--publish", action="store_true")
  parser.add_argument("--game", choices=[folder for folder, _, _ in GAMES])
  parser.add_argument("--softmax", default="softmax", help="Path to the authenticated Softmax CLI.")
  arguments = parser.parse_args()
  games = [game for game in GAMES if arguments.game in (None, game[0])]
  output = ROOT / "wiki"
  output.mkdir(exist_ok=True)
  mediaFile = output / "media.json"
  stateFile = output / "state.json"
  images = json.loads(mediaFile.read_text()) if mediaFile.exists() else {}
  state = json.loads(stateFile.read_text()) if stateFile.exists() else {}
  headers = {}
  if arguments.publish:
    token = os.environ.get("SOFTMAX_TOKEN")
    if not token:
      token = subprocess.run(
        [arguments.softmax, "get-token", "--server", SERVER],
        check=True, capture_output=True, text=True,
      ).stdout.strip()
    headers["Authorization"] = "Bearer " + token
  with httpx.Client(base_url=SERVER + "/observatory/v2/", headers=headers, timeout=30) as client:
    if arguments.publish:
      for folder, _, _ in games:
        page = ROOT / folder / "index.html"
        soup = BeautifulSoup(page.read_text(), "html.parser")
        for image in soup.find_all("img"):
          if not image.get("alt"):
            continue
          file = (page.parent / image["src"]).resolve()
          if not file.is_relative_to(ROOT):
            raise ValueError(f"Image escapes the site: {file}")
          contents = file.read_bytes()
          key = digest(contents)
          if key in images:
            continue
          response = client.post("posts/media", data={"kind": "image"}, files={
            "file": (file.name, contents, mimetypes.guess_type(file.name)[0]),
          })
          response.raise_for_status()
          storage = response.json()["s3_key"]
          if not storage.startswith("post-media/") or ".." in storage.split("/"):
            raise ValueError("Unexpected image storage location")
          images[key] = MEDIA + storage
          saveJson(mediaFile, images)
          print("Uploaded", file.relative_to(ROOT), flush=True)
    pages = []
    for folder, game, route in games:
      pages.append((folder, game, route, "game-guide", game + " — Game Guide", folder + "/", guide(folder, images)))
    if arguments.game in (None, "GOTA"):
      pages.extend([
        ("GOTA", "Gods of the Arena", "gods-of-the-arena", "hero-statistics", "Gods of the Arena — Hero Statistics", "GOTA/heros/", heroStats()),
        ("GOTA", "Gods of the Arena", "gods-of-the-arena", "player-standings", "Gods of the Arena — Player Standings", "GOTA/standings/", standings()),
      ])
    for folder, game, route, slug, title, source, content in pages:
      reference = output / "references" / folder / (slug + ".md")
      if reference.exists():
        heading = "" if slug == "game-guide" else "## Published report\n\n"
        if heading:
          content = re.sub(r"^(#{2,5}) ", r"#\1 ", content, flags=re.MULTILINE)
        content = reference.read_text().rstrip() + "\n\n---\n\n" + heading + content
      body = (
        f"Source: [Polyworld Buff]({SITE + source}). "
        "Synced snapshot; interactive views remain on the source site.\n\n"
        + content + "\n\n---\n\n"
        "Synced from Polyworld Buff by Codex.\n"
      )
      if folder == "GOTA":
        body += "\n[Game guide](game-guide) · [Hero statistics](hero-statistics) · [Player standings](player-standings)\n"
      destination = output / folder / (slug + ".md")
      destination.parent.mkdir(exist_ok=True)
      destination.write_text(body)
      print("Generated", destination.relative_to(ROOT), flush=True)
      if not arguments.publish:
        continue
      endpoint = "wikis/" + quote(game) + "/pages/" + slug
      current = client.get(endpoint)
      base = None
      key = folder + "/" + slug
      if current.status_code != 404:
        current.raise_for_status()
        current = current.json()
        previous = current["current_revision"]["body"]
        base = current["current_revision_id"]
        if previous == body and current["title"] == title:
          state[key] = {"revision": base, "title": title, "body_sha256": digest(body.encode())}
          saveJson(stateFile, state)
          print("Unchanged", key, flush=True)
          continue
        if (
          key not in state
          or digest(previous.encode()) != state[key]["body_sha256"]
          or current["title"] != state[key]["title"]
        ):
          raise RuntimeError(f"Wiki edits need merging: {key}. Local draft saved; remote page left intact.")
      payload = {
        "title": title, "body": body, "base_revision_id": base,
        "idempotency_key": digest((endpoint + str(base) + title + body).encode()),
        "note": "Sync public Polyworld Buff documentation and report snapshots (Codex).",
      }
      response = client.put(endpoint, json=payload)
      response.raise_for_status()
      verified = client.get(endpoint)
      verified.raise_for_status()
      verified = verified.json()
      if verified["current_revision"]["body"] != body or verified["title"] != title:
        raise RuntimeError(f"Wiki readback differs: {key}")
      state[key] = {"revision": verified["current_revision_id"], "title": title, "body_sha256": digest(body.encode())}
      saveJson(stateFile, state)
      print("Published", f"https://softmax.com/{route}/wiki/{slug}", flush=True)


if __name__ == "__main__":
  main()
