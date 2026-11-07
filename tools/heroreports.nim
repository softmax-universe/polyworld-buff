import
  std/[os, strutils],
  layouts

const
  SiteUrl = "https://softmax-universe.github.io/polyworld-buff/"
  # Standalone reports generated before the rename can contain this link.
  LegacyGuideUrl = "https://metta-ai.github.io/polyworld-buff/GOTA/"
  ChartAssets = ["progression.css", "progression.js"]
  ChartSection = "<section id=\"hero-progression\" " &
    "aria-label=\"Hero progression\"></section>"
  ChartRoot = currentSourcePath().parentDir.parentDir /
    "GOTA/heros/hero_assets"

type HeroReportError* = object of CatchableError

proc styleHeroReport*(html: string, standalone = false): string =
  ## Applies the shared website layout with links for disk or GitHub Pages.
  if "@@" in html or "id=\"report-data\"" notin html:
    raise newException(HeroReportError,
      "Pass the generated report, not the HTML template")
  result = html.replace(
    "<link rel=\"stylesheet\" href=\"hero_assets/site.css\">",
    "<link rel=\"stylesheet\" href=\"../site.css\">"
  )
  result = stylePage(result, HeroStats)
  if "hero_assets/progression.css" notin result:
    result = result.replace(
      "</head>",
      "<link rel=\"stylesheet\" href=\"hero_assets/progression.css\">\n" &
      "<script src=\"hero_assets/progression.js\" defer></script>\n</head>"
    )
  result = result.replace(ChartSection & "\n    ", "")
  result = result.replace(ChartSection, "")
  var position = result.find("<details id=\"methods\">")
  if position < 0:
    position = result.find("<footer")
  if position < 0:
    raise newException(HeroReportError, "Cannot find hero report content")
  result = result[0 ..< position] & ChartSection & "\n    " &
    result[position .. ^1]
  for link in ["index.html", "../index.html", SiteUrl & "GOTA/", LegacyGuideUrl]:
    result = result.replace(
      "<a href=\"" & link & "\">GOTA guide</a> · ", ""
    )
  result = result.replace(
    "Static hero report · Works offline",
    "<a href=\"../index.html\">GOTA guide</a> · " &
      "Static hero report · Works offline"
  )
  if standalone:
    result = result.multiReplace(
      ("href=\"../site.css\"", "href=\"hero_assets/site.css\""),
      ("src=\"../assets/themes/gota/gota_logo.png\"",
        "src=\"hero_assets/logo.png\""),
      ("href=\"../../\"", "href=\"" & SiteUrl & "\""),
      ("href=\"../index.html\"", "href=\"" & SiteUrl & "GOTA/\""),
      ("href=\"../heros/\"", "href=\"#\""),
      ("href=\"../standings/\"",
        "href=\"" & SiteUrl & "GOTA/standings/\""),
      ("href=\"../players/\"",
        "href=\"" & SiteUrl & "GOTA/players/\"")
    )

proc writeReport(path, html: string) =
  ## Replaces the report after the full HTML has been written successfully.
  writeFile(path & ".tmp", html)
  moveFile(path & ".tmp", path)

proc publishHeroReport*(source, root: string, refreshSource = false) =
  ## Copies only the report and artwork into the dedicated hero folder.
  let
    sourcePath = absolutePath(source)
    sourceAssets = sourcePath.parentDir / "hero_assets"
    target = absolutePath(root / "GOTA/heros/index.html")
    targetAssets = target.parentDir / "hero_assets"
    stylesheet = root / "GOTA/site.css"
  try:
    let html = styleHeroReport(readFile(sourcePath))
    if not dirExists(sourceAssets):
      raise newException(HeroReportError,
        "Missing hero_assets folder beside " & sourcePath)
    if not fileExists(stylesheet):
      raise newException(HeroReportError, "Missing stylesheet: " & stylesheet)
    createDir(target.parentDir)
    if sourceAssets != targetAssets:
      copyDir(sourceAssets, targetAssets)
    for name in ChartAssets:
      let chart = ChartRoot / name
      if absolutePath(chart) != targetAssets / name:
        copyFile(chart, targetAssets / name)
    writeReport(target, html)
    if refreshSource and sourcePath != target:
      copyFile(stylesheet, sourceAssets / "site.css")
      for name in ChartAssets:
        if sourceAssets != targetAssets:
          copyFile(targetAssets / name, sourceAssets / name)
      writeReport(sourcePath, styleHeroReport(html, standalone = true))
    echo "Updated ", target
  except OSError, IOError:
    raise newException(HeroReportError,
      "Cannot update hero report: " & getCurrentExceptionMsg())
