"""Build the four additional guides and the game directory from curated rules.

Run with python3 tools/build_game_guides.py. Artwork is checked in beside each
page. Rules were reviewed against the sibling game sources on 2026-09-29;
source links are included in each guide. This does not publish the site.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '29 September 2026'
POLYWORLD = 'https://github.com/softmax-universe/polyworld/blob/main/games/'
AWM_SOURCE = (
    'https://github.com/softmax-universe/polyworld/blob/'
    '46e74720543e6b6d17e6aa05680d744c5302fc59/examples/awm/'
)
PUDGE = 'https://github.com/softmax-universe/polyworld-pudge-wars/blob/main/'
PAINTBOT = 'https://github.com/softmax-universe/paintbot-pw/blob/main/'


def table(headers, rows, wide=False):
    """Render a scrollable, accessible reference table."""
    head = ''.join(f'<th scope="col">{escape(str(x))}</th>' for x in headers)
    body = ''
    for row in rows:
        cells = f'<th scope="row">{escape(str(row[0]))}</th>'
        cells += ''.join(f'<td>{escape(str(x))}</td>' for x in row[1:])
        body += f'<tr>{cells}</tr>\n'
    css = ' class="cards-table"' if wide else ''
    return (f'<div class="table-wrap" tabindex="0" role="region" '
            f'aria-label="{escape(headers[0])} reference table, scroll horizontally">'
            f'<table{css}><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def panels(items, two=False):
    """Render parallel explanations as cards."""
    return '<div class="grid' + (' two' if two else '') + '">' + ''.join(
        f'<article class="panel"><h3>{escape(title)}</h3><p>{body}</p></article>'
        for title, body in items) + '</div>'


def section(key, title, body, icon='stats'):
    """Render a guide section using the site's existing icon set."""
    return (key, title, f'<section id="{key}"><h2 class="section-heading">'
            f'<img src="../GOTA/assets/icons/{icon}.png" alt="">'
            f'{escape(title)}</h2>{body}</section>')


def write_guide(slug, title, genre, intro, art, facts, sections, sources,
                accent, landscape=False):
    """Write one standalone guide with shared site navigation and styling."""
    nav = ''.join(f'<a class="jump" href="#{key}">{escape(label)}</a>'
                  for key, label, _ in sections)
    facts_html = ''.join(f'<div class="fact"><dt>{escape(label)}</dt>'
                         f'<dd>{escape(value)}</dd></div>' for label, value in facts)
    source_html = ''.join(f'<li><a href="{url}">{escape(label)}</a></li>'
                          for label, url in sources)
    art_class = ' landscape' if landscape else ''
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(intro, quote=True)}">
  <title>{escape(title)} · Polyworld Buff</title>
  <link rel="stylesheet" href="../guides.css">
</head>
<body style="--accent: {accent}">
  <a class="skip" href="#guide">Skip to guide</a>
  <header class="topbar"><nav class="nav-inner" aria-label="Site navigation">
    <a class="brand" href="../">Polyworld Buff</a>
    <span class="crumb">{escape(title)} / Game guide</span>
    <a href="../">All games &rarr;</a>
  </nav></header>
  <main id="guide">
    <div class="hero">
      <div><p class="eyebrow label">{escape(genre)}</p>
        <h1>{escape(title)}</h1><p>{escape(intro)}</p>
        <a class="jump" href="#overview">Learn the game &darr;</a>
      </div>
      <div class="hero-visual"><img class="hero-art{art_class}"
        src="assets/{art}" alt="{escape(title)} artwork"></div>
    </div>
    <dl class="facts">{facts_html}</dl>
    <nav class="section-nav" aria-label="Guide sections">{nav}</nav>
    {''.join(body for _, _, body in sections)}
    <section id="sources"><h2>Sources &amp; artwork</h2>
      <p>Rules reviewed on {DATE}. This guide describes the source version
      available on that date; match settings and older replays can differ.</p>
      <ul class="sources">{source_html}</ul>
      <p class="caption"><a href="assets/sources.txt">Artwork sources</a></p>
    </section>
    <footer><p><a href="../">All seven game guides</a> · Polyworld Buff</p>
      <p>Game rules and reference. Strategy notes are suggestions, not measured rankings.</p></footer>
  </main>
</body>
</html>
'''
    (ROOT / slug / 'index.html').write_text(html)


def heartleaf():
    """Build the village, dinner, and scoring guide."""
    overview = '''<p>A week in Heartleaf is a contest of hospitality. Collect vegetables,
    arrange dinner with your neighbors, and decide when to host or visit. The villager
    with the most points after the final day wins.</p>''' + panels([
        ('Gather', 'Each of the 27 plots grows one vegetable each morning. Pick from any available garden; a harvested plot stays empty until the next day.'),
        ('Share dinner', 'Be inside a house at 18:00. A party needs its owner and at least one visitor. Everyone eats from the host’s pantry.'),
        ('Get home', 'Return to your own house by 21:00. Anyone elsewhere loses 3 points, even if they are inside another villager’s house.')])
    clock = table(['Time', 'What happens', 'Plan around it'], [
        ('09:00', 'Gardens refill; villagers begin at their doorsteps.', 'Choose a gathering route and possible dinner partners.'),
        ('09:00–18:00', 'Gather, travel, invite, accept invitations, or talk.', 'Build a pantry if hosting; leave enough time to reach dinner.'),
        ('18:00', 'Every house resolves dinner at the same instant.', 'Presence matters. An accepted invitation alone does not seat you.'),
        ('18:00–21:00', 'Evening travel continues after the meal.', 'Head to your own house before curfew.'),
        ('21:00', 'Curfew penalty and daily score tally.', 'Scores carry over into the next day.')]) + '''<p>One village day takes 3 minutes of simulation time:
        one real second advances the clock by four village minutes. The normal match
        lasts seven days; custom matches can run up to 28.</p>'''
    dinner = '''<div class="split"><div><h3>What makes a party?</h3>
    <p>The owner must be home and at least one other villager must be inside at the
    dinner bell. An empty house, a lone host, and villagers outdoors earn no dinner points.</p>
    <h3>Hosting</h3><p>Your carried vegetables become the pantry. First you earn
    <strong>pantry items × visitors</strong>. You also join the meal. Hosting empties
    your inventory; visitors keep theirs.</p>
    <h3>Eating</h3><p>Dinner has three bite rounds. Each diner can receive one item per
    round while food remains. Seating is shuffled deterministically. A bite favors
    vegetable types you have not tasted this week.</p>
    <p>A first taste earns 3 points; another bite of a familiar vegetable earns 1.
    The set of tasted vegetables persists throughout the match.</p></div>
    <aside class="panel"><h3>A dinner example</h3><p>You bring 6 vegetables and host
    2 visitors. Your hospitality bonus is <strong>6 × 2 = 12 points</strong>.</p>
    <p>The three of you then share those six items across the bite rounds. Each
    diner earns their own tasting points; those points are added to your hosting
    bonus if you are the host.</p><p>Guests do not pay with their own vegetables.
    A small pantry can run out before everyone gets three bites.</p></aside></div>'''
    score = table(['Scoring event', 'Points', 'Condition'], [
        ('Hosting', 'Items in pantry × number of visitors', 'Owner and at least one visitor are in the house at 18:00.'),
        ('First taste', '+3 per bite', 'First time this villager eats that vegetable type during the match.'),
        ('Repeat taste', '+1 per bite', 'This villager has already tasted that type.'),
        ('Missed curfew', '−3', 'Not in your own house at 21:00.'),
        ('Winner', 'Highest accumulated score', 'After the final day; scores may be negative.')], True)
    veggies = ['Carrot', 'Tomato', 'Lettuce', 'Potato', 'Pumpkin', 'Radish', 'Beet', 'Corn', 'Pea', 'Onion', 'Garlic', 'Cabbage', 'Squash', 'Turnip', 'Leek', 'Spinach', 'Broccoli', 'Pepper', 'Cucumber', 'Zucchini', 'Celery', 'Eggplant', 'Parsnip', 'Kale']
    village = '''<div class="split"><div><h3>Nine neighbors</h3><p>Ivan, Anton, Yura,
    Sasha, Maxim, Nikita, Vova, Dima, and Egor each have a house with three garden plots.</p>
    <h3>24 vegetables</h3><p>Variety matters because every villager tracks their own
    first tastes. Vegetables left in your inventory carry into later days unless
    you host dinner.</p><div class="tags">''' + ''.join(f'<span class="tag">{v}</span>' for v in veggies) + '''</div>
    <h3 style="margin-top:24px">Invitations and conversation</h3><p>Invite or accept
    within 3 tiles. An invitation records intent, but never moves someone or binds
    them to attend. Talk within 4 tiles in groups of up to four. Gathering and
    entering a door require being within 1 tile.</p></div><figure>
    <img class="village-art" src="assets/village.png" loading="lazy" alt="Heartleaf village terrain artwork showing nine houses around a central tree">
    <figcaption>Village terrain artwork. Each home has three garden plots.</figcaption></figure></div>'''
    tips = panels([
        ('Host with a plan', 'A full basket becomes much more valuable when visitors actually arrive. Arrange company early and be home before the bell.'),
        ('Visit for variety', 'An invitation can save your pantry for another day while letting you collect new tastes from someone else’s meal.'),
        ('Watch the clock', 'Dinner and curfew are hard deadlines. A great gathering route is only useful if you can still reach the right house.')])
    write_guide('Heartleaf', 'Heartleaf', 'Village life · Gathering · Dinner parties',
        'Gather vegetables, invite your neighbors, and turn a week of shared dinners into the highest score in the village.',
        'logo.png', [('Villagers', '9'), ('Default match', '7 days'), ('Dinner bell', '18:00'), ('Curfew', '21:00')],
        [section('overview', 'How to play', overview, 'champion'), section('day', 'A day in Heartleaf', clock, 'move'),
         section('dinner', 'Dinner & hospitality', dinner, 'chalice'), section('scoring', 'Scoring', score, 'victory'),
         section('village', 'Village & vegetables', village, 'minion'), section('tips', 'Strategy notes', tips)],
        [('Game rules', POLYWORLD + 'heartleaf/plan.md'), ('Constants & vegetables', POLYWORLD + 'heartleaf/content.nim'),
         ('Dinner simulation', POLYWORLD + 'heartleaf/sim.nim')], '#bbdea0')


def awm():
    """Build the three-class card game and its complete base-set reference."""
    overview = '''<p>Archers Warriors Mages is a two-player card battler. Each player
    chooses one of three classes and uses its fixed 40-card deck. Play minions,
    cast spells, and protect your hero while building a winning board.</p>''' + panels([
        ('Start the duel', 'Both heroes begin with 20 life and five cards. The first player is chosen randomly and skips their first turn’s draw.'),
        ('Build your turn', 'At the start of each turn, maximum energy increases by one, energy refills, and you draw a card. Spend energy to play cards from your hand.'),
        ('Win', 'Reduce the opposing hero to zero life. A player also loses if they must draw from an empty deck.')])
    classes = '''<p>These are fixed class decks, with 40 cards each. Minion stats below
    are written as power / toughness. Copies are the number of that card in the starting deck.</p><div class="grid">'''
    for title, art, description in [
        ('Archer', 'sniper', 'Ranged minions avoid return damage from melee fighters. Bolt pressures heroes while Hail of Arrows clears fragile enemy boards.'),
        ('Warrior', 'bear', 'Efficient minions, permanent team buffs, and extra Footsoldiers build a wide board. Duel can turn a small advantage into a favorable fight.'),
        ('Mage', 'primordial', 'Bounce effects, card draw, and protective Bubbles buy time. Primordial offers a huge body and sends the rest of the board back to hand.')]:
        classes += f'<article class="panel"><img class="panel-art" src="assets/{art}.png" loading="lazy" alt="{title} card illustration"><h3>{title}</h3><p>{description}</p></article>'
    classes += '</div>'
    combat = table(['Rule', 'How it works'], [
        ('Minions', 'Attack once per turn, starting on the turn after they enter play. They can attack an enemy hero or minion.'),
        ('Damage', 'Minions exchange combat damage. Damage remains on a surviving minion; zero toughness sends it to the discard pile.'),
        ('Ranged', 'A ranged minion takes no combat damage from a non-ranged minion, whether attacking or defending. Spell and on-play damage still apply.'),
        ('Permanent changes', 'Power/toughness buffs and lost keywords last while the card stays in play. Bouncing it to hand restores its printed state.'),
        ('Summoning', 'Summoned minions arrive on the right of your board, cannot attack immediately, and do not fire their own on-play rules.'),
        ('Trinkets', 'Board cards that are not minions. They cannot attack or be attacked and are ignored by effects that target only minions.'),
        ('Next-turn triggers', 'Resolve after your normal draw, provided the triggering card remains in play.'),
        ('Duel', 'Choose its targets in order. The forced fight does not consume a minion’s normal attack.')])
    headers = ['Card', 'Energy', 'Type / stats', 'Copies', 'Effect']
    archer = table(headers, [
        ('Bolt', 1, 'Spell', 10, 'Deal 2 damage to a hero.'),
        ('Sniper', 2, 'Minion · 2 / 1', 14, 'Ranged.'),
        ('Sharpshooter', 3, 'Minion · 3 / 1', 10, 'Ranged. On play: deal 1 damage to a minion or hero.'),
        ('Hail of Arrows', 3, 'Spell', 6, 'Deal 1 damage to every enemy minion.')], True)
    warrior = table(headers, [
        ('Bear', 2, 'Minion · 3 / 2', 8, 'No additional effect.'),
        ('Swords', 2, 'Spell', 5, 'Give all friendly minions +1 power.'),
        ('Shields', 1, 'Spell', 4, 'Give all friendly minions +1 toughness.'),
        ('Duel', 2, 'Spell', 5, 'Give the first target minion +1/+1. The second loses Ranged. Then the two fight.'),
        ('Tactician', 2, 'Minion · 1 / 2', 5, 'On play: reduce a target minion’s power by 1.'),
        ('Footsoldier', 1, 'Minion · 1 / 2', 6, 'No additional effect.'),
        ('Commander', 5, 'Minion · 2 / 3', 4, 'On play: summon two Footsoldiers.'),
        ('Rally', 5, 'Spell', 3, 'Summon two Footsoldiers, then give all friendly minions +1 power.')], True)
    mage = table(headers, [
        ('Bouncer', 1, 'Minion · 1 / 1', 16, 'On play: return a minion to its owner’s hand.'),
        ('Oozification', 4, 'Spell', 4, 'Destroy a minion. Its owner summons one Ooze per point of its current toughness.'),
        ('Plan', 3, 'Trinket', 7, 'Draw one card now. At your next turn, draw one more and destroy Plan.'),
        ('Study', 2, 'Spell', 7, 'Draw two cards, then choose one card to discard.'),
        ('Primordial', 8, 'Minion · 10 / 10', 2, 'On play: return all other board cards to their owners’ hands.'),
        ('Bubble Shield', 2, 'Spell', 4, 'Summon two Bubbles.')], True)
    tokens = table(['Token', 'Type / stats', 'Effect'], [
        ('Ooze', 'Minion · 0 / 1', 'Summoned by Oozification; not included in the starting deck.'),
        ('Bubble', 'Trinket', 'When its owner’s hero is attacked, return the attacker to its owner’s hand and destroy this Bubble. Not included in the starting deck.')])
    tips = panels([
        ('Archer: pick clean fights', 'Trade ranged minions into non-ranged attackers when it improves your board, and count your remaining direct damage before committing Bolt.'),
        ('Warrior: build before buffing', 'Swords and Shields affect every friendly minion already in play. Rally summons before its buff, so the new Footsoldiers benefit too.'),
        ('Mage: buy time carefully', 'Bounce can rescue or reset a friendly minion as well as delay an enemy. Watch your deck size: extra draws can become dangerous near deck-out.')])
    write_guide('AWM', 'Archers Warriors Mages', 'Card battler · Three classes · Fixed decks',
        'Choose a class, spend energy, and build a board of minions, spells, and trinkets in a head-to-head card duel.',
        'sniper.png', [('Players', '2'), ('Starting life', '20'), ('Deck size', '40 cards'), ('Opening hand', '5 cards')],
        [section('overview', 'How to play', overview, 'champion'), section('classes', 'The three classes', classes, 'minion'),
         section('combat', 'Turns & combat', combat, 'attack'), section('archer', 'Archer cards', archer, 'range'),
         section('warrior', 'Warrior cards', warrior, 'damage'), section('mage', 'Mage cards', mage, 'mana'),
         section('tokens', 'Summoned tokens', tokens, 'minion'), section('tips', 'Strategy notes', tips)],
        [('Card definitions & deck lists', AWM_SOURCE + 'baseset.nim'), ('Turn & victory rules', AWM_SOURCE + 'awmsim.nim'),
         ('Rules engine', AWM_SOURCE + 'awmcore.nim')], '#e2c597', landscape=True)


def pudge():
    """Build the hook arena, upgrade, and shop reference."""
    overview = '''<p>Two teams of butchers face each other across a river. Catch an
    enemy with Meat Hook, pull them into danger, and finish the fight together.
    Rescue teammates with the same hook, dodge incoming throws, and turn kills into upgrades.</p>''' + panels([
        ('Take the lead', 'The standard hosted match is 3v3, first to 30 team kills, with a 20-minute limit. A hosted 1v1 duel uses 10 kills and an 8-minute limit.'),
        ('Survive the river', 'The river deals 30 damage every half-second. Blink cannot cross directly from one bank to the other; river landings are possible but dangerous.'),
        ('Reset and return', 'Respawn after 4 seconds. The 2-second spawn shield ends early when you walk, hook, or attack. Your own fountain heals you while you idle on its pad.')])
    abilities = table(['Ability', 'Base numbers', 'What it does'], [
        ('Meat Hook', '200 damage · 60-tile range · about 2.03 s cooldown', 'Wind up for about 0.28 s, then throw and reel in the first valid catch. Hooking a teammate heals them for 120.'),
        ('Melee attack', '28 damage · about 0.59 s between attacks', 'Finish enemies pulled into close range.'),
        ('Grapple', '20-tile range · 6 s cooldown', 'Latch onto terrain and pull yourself toward it. Does no damage.'),
        ('Rot', '24 damage every 0.5 s · 8-tile radius · 40% slow', 'Toggle a cloud that damages everyone inside, including yourself. It can kill you.'),
        ('Blink', 'Up to 20 tiles · 8 s cooldown', 'Hop toward a target. Cliffs, walls, and bodies can shorten the hop; a direct bank-to-bank crossing is disallowed.')], True)
    survival = table(['Feature', 'Rule'], [
        ('Starting health', '840 HP, with 35 additional maximum HP per level.'),
        ('Home fountain', 'Recover 2% of maximum HP every half-second while idling on your own spawn pad.'),
        ('Island fountain', 'Recover 1.5% of maximum HP per second within 16 tiles of the central island fountain.'),
        ('River damage', 'Lose 30 HP every half-second while drowning.'),
        ('Fog of war', 'Your own bank and the river are visible. Living allies and wards reveal nearby enemy-bank positions within 20 tiles.'),
        ('Self-kill with Rot', 'The other team gains a kill toward its goal; nobody receives the personal kill, upgrade point, or gold bounty.')])
    upgrades = '''<p>An enemy kill earns the killer one upgrade point. Spend one point
    for one rank; each of the four hook upgrades caps at rank 10. Shop gold is a
    separate resource.</p>''' + table(['Upgrade', 'Benefit'], [
        ('Damage', '+15 enemy hook damage per rank, starting at 200.'),
        ('Distance', '+4 tiles of hook range per rank, starting at 60.'),
        ('Speed', 'Faster hook flight and reeling.'),
        ('Radius', '+0.125 tiles of catch radius per rank, starting at 2.75.')]) + '''<p>Enemy kills pay 3 base gold, with extra bounty for first blood,
    streaks, and shutdowns. A successful mid-air hook deflection pays 1 gold.
    Buy shop items while in range of your base shop.</p>'''
    runes = '''<p>A river rune appears every 20 seconds, beginning at 0:20. Location
    and kind follow a fixed cycle. Combat buffs last 15 seconds; Bounty pays
    immediately and does not replace your current combat buff.</p>''' + table(['Rune', 'Effect'], [
        ('Haste', '+40% movement speed.'),
        ('Double Damage', 'Double hook damage.'),
        ('Regeneration', 'Recover 3% of maximum HP every half-second.'),
        ('Big Hook', '+50% hook range, catch radius, and hook damage.'),
        ('Lightning', 'Hook hit adds 120 splash damage within 8 tiles.'),
        ('Bounty', 'Gain 4 gold immediately.')])
    shop = table(['Item', 'Gold', 'Effect'], [
        ('Healing Flask', 5, 'Instantly restore full health.'),
        ('Haste', 4, 'Apply the timed movement-speed buff.'),
        ('Regeneration', 4, 'Apply the timed regeneration buff.'),
        ('Big Hook', 6, 'Apply the timed hook-size and damage buff.'),
        ('Double Damage', 8, 'Apply the timed hook-damage buff.'),
        ('River Treads', 10, '+8% movement speed per rank.'),
        ('Longflight Brand', 12, '+1% hook damage per tile traveled, per rank.'),
        ('Bank Palisade', 10, 'Place a temporary wall with health on your bank. Higher ranks improve it.'),
        ('Hooktrap', 10, 'Place a hidden mine. Enemy hooks detonate it; allied hooks can grab it.'),
        ('Farwatch Ward', 8, 'Place a 45-second vision ward on either bank. Up to two wards per player.')]) + '''<p>The five permanent item families each occupy one inventory slot.
    Buying a family again increases its rank, up to five. Flasks and timed buffs
    do not occupy those slots.</p>'''
    tips = panels([
        ('Aim where they will be', 'Hooks have a visible windup and travel time. Lead moving targets, vary your own movement, and use terrain to break easy lines.'),
        ('Hook for your team', 'An allied hook both repositions and heals. A rescue can deny an enemy kill and preserve your team’s pressure.'),
        ('Spend around your plan', 'Damage helps secure kills, but range, radius, and speed change which catches you can land. Contest the predictable rune timer.')])
    write_guide('PudgeWars', 'Pudge Wars', 'Hook arena · Team combat · River control',
        'Land hooks across the river, rescue allies, and upgrade your butcher in a race to the team kill goal.',
        'logo.png', [('Standard teams', '3 vs 3'), ('Kill goal', '30'), ('Starting health', '840 HP'), ('Respawn', '4 seconds')],
        [section('overview', 'How to play', overview, 'champion'), section('abilities', 'Abilities', abilities, 'attack'),
         section('survival', 'Survival & vision', survival, 'health'), section('upgrades', 'Upgrades & gold', upgrades, 'experience'),
         section('runes', 'River runes', runes, 'mana'), section('shop', 'Base shop', shop, 'gold'),
         section('tips', 'Strategy notes', tips)],
        [('Hosted match settings', PUDGE + 'coworld/coworld_manifest_template.json'), ('Abilities & item constants', PUDGE + 'examples/pudge_wars/content.nim'),
         ('Combat simulation', PUDGE + 'examples/pudge_wars/sim.nim')], '#b9da91')


def paintbot():
    """Build the current team-mode territory and glory reference."""
    overview = '''<p>Paintbot PW’s team game takes place in Heartwick. Sixteen wheeled
    cogs split into red and blue teams, contest heart towers, and use paint weapons
    to keep opponents away. This guide covers the standard team game; the separate
    Heartland free-for-all variant has different rules.</p>''' + panels([
        ('Capture territory', 'The baseline island has ten hearts. Each team starts with one home heart; eight begin neutral. Stand near a heart for three uncontested seconds to claim it.'),
        ('Fill the heart meter', 'Each owned heart earns one point per second. Reach 900 points first, or have the higher meter when the ten-minute limit expires.'),
        ('Keep your crew alive', 'Each cog has 3 HP and three respawns, for four lives total. A team loses immediately once every cog is out with no respawns remaining.')])
    capture = table(['Capture rule', 'What happens'], [
        ('Range', 'Stay within 140 world units (1.4 tiles), with a traversable connection to the heart.'),
        ('Capture time', '3 seconds / 72 ticks. Extra friendly cogs do not speed it up.'),
        ('Contested heart', 'Both teams in range pause capture progress.'),
        ('Leaving', 'If attackers leave or only defenders remain, capture progress resets.'),
        ('Income', 'The old owner keeps earning until the capture completes.'),
        ('All ten hearts', 'Income increases to 10 points per second, but the game does not end immediately.'),
        ('Public information', 'Heart positions, ownership, capture progress, and whether a heart is contested are visible to everyone.')]) + '''<div class="note"><strong>Five hearts for three minutes = 900 points.</strong>
    The meter measures accumulated control, so an early lead still counts after you
    lose territory. Generated map variants can have different heart layouts and counts.</div>'''
    scoring = '''<p>The heart meter decides the winning team. <strong>Glory is the
    match score and ladder input.</strong> Only the winner keeps its glory; the
    losing team and both sides of a draw score zero.</p>''' + table(
        ['Glory event', 'Current Competition setting', 'Engine default'], [
        ('Starting glory', 'Match length in seconds: 600 in a ten-minute game', 'Same'),
        ('Time passing', '−1 each second', 'Same'),
        ('No supplies collected', '+10 every 30 seconds without collecting a supply', 'Same'),
        ('Glory heart pickup', '+20', 'Same'),
        ('Trailing in remaining lives', '+5 per life behind, every 5 seconds', '+1 per life behind, every 5 seconds'),
        ('Trailing in active cogs', '+10 per additional eliminated cog, every 5 seconds', '+1 per additional eliminated cog, every 5 seconds'),
        ('Loss or draw', 'Final glory becomes 0', 'Same')], True) + '''<p>“Eliminated” means dead with no lives left. These bonuses reward winning
    despite disadvantages. Taking friendly fire no longer awards glory in the
    current rules. Match configuration can override the award amounts.</p>
    <p>At the time limit, the higher heart meter wins; equal totals draw. If both
    meters fill on the same tick, compare their totals. If both teams are eliminated
    on the same tick, compare the meters without awarding an elimination bonus.</p>'''
    combat = table(['Weapon / equipment', 'Numbers', 'How it works'], [
        ('Paintball gun', '5-tick windup · 1 shot/second · 5,250-unit range', 'Aim locks during windup, then a hitscan ray resolves. Friendly fire is enabled; simultaneous shots choose targets before damage.'),
        ('Grenade', 'Up to 1-second charge · 10-tick flight · 3 damage', 'Explodes in a 360-unit radius under the current strong-grenade rules. Grenade pickups return after 5 seconds.'),
        ('Spray', '850-unit reach · 5-tick burst · 3 damage', 'Replaces the gun while carried. Aim stays locked for the burst; each victim is hit once, followed by an 8-tick recovery.'),
        ('Shield pickup', '3 armor', 'Armor absorbs damage before HP. It does not heal you. Pickup respawns after 30 seconds.'),
        ('Medkit', 'Restore base HP', 'Healthy cogs ignore it. Pickup respawns after 30 seconds.')], True) + '''<p>The game runs at 24 ticks per second. One Polyworld tile is 100 world
    units, so the gun reaches 52.5 tiles and spray reaches 8.5 tiles.</p>'''
    field = '''<div class="split"><div><h3>Vision and cover</h3>
    <p>Standard vision is a forward-facing 120-degree cone with unlimited distance
    and wall occlusion. Matches can opt into shared team vision instead. Facing
    and terrain matter when identifying threats.</p>
    <h3>Trenches</h3><p>When fired at from outside a trench, 70% of gunfire passes
    over it. Leaving a trench is five times slower and its fire cooldown is tripled.
    Spray ignores trench cover. A grenade deals 6 damage in its own trench,
    2 into another trench, and 3 outside trenches.</p>
    <h3>Respawning</h3><p>Death removes equipment. Respawn takes 3 seconds, followed
    by 1.5 seconds of spawn protection. Cogs spawn near an owned heart, favoring
    less-covered positions; with no owned heart, they use their endzone.</p>
    </div><figure><img src="assets/heartwick.png" loading="lazy"
    alt="Heartwick concept artwork with red and blue cogs, heart towers, winding paths, and cottages">
    <figcaption>Heartwick concept artwork, not a screenshot or tactical map.</figcaption></figure></div>'''
    variants = table(['Mode / variant', 'What changes'], [
        ('Competition', 'Sixteen cogs, eight per team, using the current glory awards above.'),
        ('Two policy teams', 'Two policies control the two teams; the battlefield still contains sixteen cogs.'),
        ('Two captains per team', 'Control is split between two captains on each team; sixteen cogs remain on the battlefield.'),
        ('Map variants', 'Twin Mesas, Archipelago, Serpent River, Crater, Terraces, Deep Forest, Badlands, Atoll, Highlands, and Delta change the terrain.'),
        ('Large maps', 'Big Deep Forest and Big Twin Mesas offer larger configurations. Check each match’s roster and map settings.')])
    tips = panels([
        ('Spread out with purpose', 'More cogs on one heart do not capture it faster. Cover several objectives while keeping enough support to hold contested ground.'),
        ('Track income and lives', 'A kill helps when it protects capture time or removes enemy pressure. Spending all your lives for a brief fight can lose the match immediately.'),
        ('Secure the win first', 'Glory survives only on the winning side. Weigh a risky pickup or handicap against the heart-meter lead you need to keep it.')])
    write_guide('Paintbot', 'Paintbot PW', 'Heartwick · Territory control · Paint combat',
        'Lead a crew of wheeled cogs, capture heart towers, and hold the island long enough to turn control into victory.',
        'paint-crew.png', [('Standard teams', '8 vs 8'), ('Baseline hearts', '10'), ('Winning meter', '900 points'), ('Match limit', '10 minutes')],
        [section('overview', 'How to play', overview, 'champion'), section('hearts', 'Hearts & territory', capture, 'tower'),
         section('scoring', 'Winning & glory', scoring, 'victory'), section('equipment', 'Combat & equipment', combat, 'attack'),
         section('field', 'Vision, terrain & lives', field, 'health'), section('variants', 'Team variants', variants, 'minion'),
         section('tips', 'Strategy notes', tips)],
        [('Hosted rules & variant settings', PAINTBOT + 'coworld/paintbot/coworld_manifest_template.json'),
         ('Simulation & scoring', PAINTBOT + 'examples/paintbot/sim.nim'),
         ('Combat mechanics', PAINTBOT + 'examples/paintbot/mechanics.nim'),
         ('Artwork provenance', PAINTBOT + 'docs/paintbot-art.md')], '#a1d8ee')


def home():
    """Build the seven-game directory without changing the existing guides."""
    games = [
        ('GOTA', 'Gods of the Arena', 'GOTA/assets/themes/gota/gota_logo.png',
         'Meet the heroes, explore their abilities, and learn the arena.', False),
        ('LvD', 'Light vs Dark', 'LvD/assets/themes/lvd/lvd_logo.png',
         'Compare the factions, units, buildings, and match rules.', False),
        ('CTA', 'Call to Adventure', 'CTA/assets/themes/cta/cta_logo.png',
         'Discover the party, dungeon monsters, abilities, and loot.', False),
        ('Heartleaf', 'Heartleaf', 'Heartleaf/assets/logo.png',
         'Gather vegetables, host dinner parties, and get to know the village.', False),
        ('AWM', 'Archers Warriors Mages', 'AWM/assets/sniper.png',
         'Explore three classes, every base-set card, and the rules of the duel.', True),
        ('PudgeWars', 'Pudge Wars', 'PudgeWars/assets/logo.png',
         'Land hooks, control the river, and compare abilities, runes, and upgrades.', False),
        ('Paintbot', 'Paintbot PW', 'Paintbot/assets/paint-crew.png',
         'Capture hearts with your paint crew and learn how territory and glory score.', False)]
    cards = ''
    for slug, title, art, description, landscape in games:
        css = ' class="landscape"' if landscape else ''
        cards += f'''<a class="game" href="{slug}/">
          <img{css} src="{art}" alt="" loading="lazy">
          <h2>{escape(title)}</h2><p>{escape(description)}</p>
          <span class="game-link">Read the guide &rarr;</span></a>\n'''
    (ROOT / 'index.html').write_text(f'''<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Game guides for Gods of the Arena, Light vs Dark, Call to Adventure, Heartleaf, Archers Warriors Mages, Pudge Wars, and Paintbot PW.">
  <title>Polyworld Buff</title><link rel="stylesheet" href="guides.css">
</head><body><main>
  <nav class="home-nav" aria-label="Main navigation"><a href="#game-guides" aria-current="page">Game guides</a><a href="engine/">Polyworld Engine ↗</a></nav>
  <header class="home-header"><p class="eyebrow label">Seven games. One place to learn.</p>
    <h1>Polyworld Buff</h1><p>Explore the games. Learn the characters, cards,
    abilities, and rules. Pick a guide to get started.</p></header>

  <a class="engine-promo" href="engine/">
    <div><p class="eyebrow label engine-promo-nim">Built with <img src="engine/assets/nim-logo.svg" alt="Nim" width="104" height="28"><span class="engine-promo-softmax"><img src="engine/assets/softmax-brand-mark.svg" alt="" width="28" height="28">Softmax</span></p><h2>A 3D game engine, written in Nim.</h2><p>Readable code, native compilation, and worlds you can play. Explore Polyworld and the games built with it.</p><span class="game-link">Discover Polyworld Engine &rarr;</span></div>
    <img src="engine/assets/gota.jpg" alt="A hero and soldiers on a forest lane in Gods of the Arena." width="1280" height="720">
  </a>
  <nav id="game-guides" class="games" aria-label="Game guides">{cards}</nav>
  <footer><p><a href="https://github.com/softmax-universe/polyworld-buff">View on GitHub</a></p></footer>
</main></body></html>
''')


def main():
    """Regenerate the new guides and home page together."""
    heartleaf()
    awm()
    pudge()
    paintbot()
    home()
    print('Built Heartleaf, AWM, PudgeWars, Paintbot, and the seven-game directory.')


if __name__ == '__main__':
    main()
