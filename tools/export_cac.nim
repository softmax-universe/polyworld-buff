import
  std/[options, os, strutils],
  jsony, pixie,
  core/[core, cardset, sim], ui/cardfaces

type
  GuideCard = object
    name, slug, heroClass, kind, rules: string
    energy, power, toughness, preconCopies: int
    levelUp: bool

  GuideData = object
    startingLife, openingHand, deckSize, maxCopies, offClassCost: int
    cards: seq[GuideCard]

proc exportCards() =
  ## Exports the current base set and renders matching card faces.
  var data = GuideData(
    startingLife: StartingLife,
    openingHand: StartingHandSize,
    deckSize: DeckSize,
    maxCopies: MaxCopies,
    offClassCost: OffClassCost
  )

  let arguments = commandLineParams()
  doAssert arguments.len == 2, "Pass the card asset root and output directory."
  initCardAssets(arguments[0])
  createDir(arguments[1] / "cards")

  for card in baseCards:
    var entry = GuideCard(
      name: card.name,
      slug: card.name.toLowerAscii().replace(" ", "-"),
      kind: $card.kind,
      rules: card.ruleText(),
      energy: card.energyCost,
      levelUp: card.levelUpClass.isSome
    )
    if card.kind == Minion:
      entry.power = card.power
      entry.toughness = card.toughness
    if card.class.isSome:
      let heroClass = card.class.get
      entry.heroClass = $heroClass
      for (name, copies) in baseDeckLists[heroClass]:
        if name == card.name:
          entry.preconCopies = copies
    data.cards.add entry
    renderCardFace(card).resize(300, 425).writeFile(
      arguments[1] / "cards" / (entry.slug & ".png")
    )

  writeFile(arguments[1] / "cards.json", data.toJson())
  echo "Exported ", data.cards.len, " cards and their current rules."

exportCards()
