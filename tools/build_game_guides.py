"""Build the four additional guides and the game directory from curated rules.

Run with python3 tools/build_game_guides.py. Artwork is checked in beside each
page. Each guide includes its own review date and source links. Cards and
Casters reads card data exported from the game. This does not publish the site.
"""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '29 September 2026'
POLYWORLD = 'https://github.com/softmax-universe/polyworld/blob/main/games/'
CAC_SOURCE = POLYWORLD + 'cac/'
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
                accent, landscape=False, reviewed=DATE, stylesheet=None,
                body_class='', hero_visual=None):
    """Write one standalone guide with shared site navigation and styling."""
    nav = ''.join(f'<a class="jump" href="#{key}">{escape(label)}</a>'
                  for key, label, _ in sections)
    facts_html = ''.join(f'<div class="fact"><dt>{escape(label)}</dt>'
                         f'<dd>{escape(value)}</dd></div>' for label, value in facts)
    source_html = ''.join(f'<li><a href="{url}">{escape(label)}</a></li>'
                          for label, url in sources)
    art_class = ' landscape' if landscape else ''
    extra_styles = f'\n  <link rel="stylesheet" href="{stylesheet}">' if stylesheet else ''
    visual = hero_visual or (f'<img class="hero-art{art_class}" '
                            f'src="assets/{art}" alt="{escape(title)} artwork">')
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(intro, quote=True)}">
  <title>{escape(title)} · Polyworld Buff</title>
  <link rel="stylesheet" href="../guides.css">{extra_styles}
</head>
<body{f' class="{body_class}"' if body_class else ''} style="--accent: {accent}">
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
      <div class="hero-visual">{visual}</div>
    </div>
    <dl class="facts">{facts_html}</dl>
    <nav class="section-nav" aria-label="Guide sections">{nav}</nav>
    {''.join(body for _, _, body in sections)}
    <section id="sources"><h2>Sources &amp; artwork</h2>
      <p>Rules reviewed on {reviewed}. This guide describes the source version
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
    """Build Cards and Casters from the game's exported card definitions.

    tools/export_cac.nim writes AWM/assets/cards.json and card images using
    games/cac/src/core and ui/cardfaces from the sibling Polyworld checkout.
    The AWM path stays stable for existing links.
    """
    data = json.loads((ROOT / 'AWM/assets/cards.json').read_text())
    cards = data['cards']
    overview = '''<p>Cards and Casters is a card game for two to seven heroes.
    Play a duel or join a multiplayer table where the last hero standing wins.
    Pick Archer, Warrior or Mage, then use a ready-made deck or build your own
    from the full base set.</p>''' + panels([
        ('Take your seat', 'Every hero starts with 20 life, a 40-card deck and five cards in hand. The first player is chosen randomly and skips the first turn’s draw. Living seats then take turns in order.'),
        ('Build your turn', 'Your total energy rises by one with no cap, your energy refills, you draw a card, and start-of-turn triggers resolve. Play affordable cards and attack with ready minions in any order. Ending your turn resolves end-of-turn triggers.'),
        ('Be the last hero standing', 'A hero is eliminated at zero life or after drawing from an empty deck. Their hand is discarded and their turns stop, but their cards in play remain. If the final heroes fall together, the current player wins.')])
    classes = '<div class="grid">'
    for title, art, description in [
        ('Archer', 'sharpshooter', 'Ranged attacks, Hidden minions and direct damage. Post can give small Archer minions Ready and summon copies, while Wildfire wears down the whole table.'),
        ('Warrior', 'commander', 'Build a board of efficient minions, summon Footsoldiers and strengthen them together. Banner keeps reinforcements coming, and Pillage removes troublesome trinkets.'),
        ('Mage', 'spirit', 'Bounce minions, draw cards and reshape the board. Control steals an opposing minion; Summon Primordial clears one hero’s board before creating your own 10/10.')]:
        classes += f'''<article class="panel"><a href="assets/cards/{art}.png" aria-label="View {art.replace('-', ' ')} card"><img class="panel-art" src="assets/cards/{art}.png" width="300" height="425" loading="lazy" alt="{title} card from the current game"></a><h3>{title}</h3><p>{description}</p></article>'''
    classes += '</div>'
    decks = '''<p>Your deck must contain exactly 40 base-set cards. Include one to
    four copies of each card you choose; the Archer, Warrior and Mage level-up
    trinkets may appear any number of times. Cards from every class are legal.
    An invalid bot deck is eliminated before the first turn.</p>
    <div class="note"><strong>Off-class cost = printed cost + max(0, 3 − class levels).</strong>
    <p>A card from your hero’s class costs its printed energy. A card from another
    class costs three extra energy, reduced by the levels in that class granted
    by cards you control. Classless cards have no surcharge.</p>
    <p>For example, a Warrior pays 5 energy for the 2-energy Sniper. With two Archer
    level-up trinkets in play, that becomes 3; with three, it returns to 2.</p></div>
    <p>The reference decks still contain 40 cards each. The card tables show their
    exact copy counts. A dash means the card is absent from that preconstructed
    deck, not that it is forbidden in a custom deck.</p>'''
    combat = table(['Rule', 'How it works'], [
        ('Minions', 'Attack an opponent’s hero or minion once per turn, normally starting on your next turn after they enter play. You can choose among opponents at a multiplayer table.'),
        ('Damage', 'Minions deal their power to each other simultaneously. Damage remains on survivors; zero toughness sends a minion to its original owner’s discard pile.'),
        ('Ranged', 'Takes no combat damage from a non-Ranged minion, whether attacking or defending. Damage from card effects still applies.'),
        ('Hidden N / Hidden', 'Cannot be attacked for N more of its controller’s turns, or indefinitely for plain Hidden. Card effects can still target it, and it can attack normally.'),
        ('Ready', 'Can attack on the turn it enters play. It still only gets one normal attack per turn.'),
        ('Lasts N', 'Leaves play as the Nth of its controller’s turns ends, counting the turn it entered.'),
        ('Trinkets', 'Stay on the board but cannot attack or be attacked. Effects that target only minions skip them; trinket-targeting effects can still remove them.'),
        ('Summoning', 'Summoned cards enter at the right of the board. Their on-play rules resolve for their controller after the summoning effect. Minions still need Ready to attack immediately.'),
        ('Control and ownership', 'A stolen or gifted card keeps its damage and changes. A transferred minion waits until its new controller’s next turn to attack. Bouncing or destroying it returns it to its original owner’s hand or discard pile.'),
        ('Changes and bounce', 'Damage, buffs and gained or lost rules persist while a card stays in play. Returning it to hand restores its printed state.'),
        ('Duel', 'A forced fight exchanges combat damage without using either minion’s normal attack. Choose its two targets in order.'),
        ('Targets and triggers', 'Resolve choices in the order requested. Discard choices and triggered effects can require decisions during another player’s turn; finish them before play continues.')])

    def card_table(selected):
        """Render live card text and artwork beside costs and deck counts."""
        rows = []
        for card in selected:
            stats = card['kind']
            if stats == 'Minion':
                stats += f" · {card['power']} / {card['toughness']}"
            rules = escape(card['rules'] or 'No additional effect.').replace('\n', '<br>')
            copies = str(card['preconCopies']) if card['preconCopies'] else '—'
            rows.append(f'''<tr data-card="{escape(card['name'], quote=True)}"><th scope="row"><a class="card-preview" href="assets/cards/{card['slug']}.png"><img src="assets/cards/{card['slug']}.png" width="300" height="425" loading="lazy" alt=""><span>{escape(card['name'])}</span></a></th><td>{card['energy']}</td><td>{stats}</td><td>{copies}</td><td>{rules}</td></tr>''')
        return '''<div class="table-wrap" tabindex="0" role="region" aria-label="Card reference table, scroll horizontally"><table class="cards-table"><thead><tr><th scope="col">Card</th><th scope="col">Energy</th><th scope="col">Type / power / toughness</th><th scope="col">Precon copies</th><th scope="col">Printed rules</th></tr></thead><tbody>''' + '\n'.join(rows) + '</tbody></table></div>'

    levelups = '''<p>These classless, zero-cost trinkets each grant one level in the
    named class while they remain in play. They reduce off-class costs and have
    no four-copy limit.</p>''' + card_table([card for card in cards if card['levelUp']])
    reference = '''<p>All {count} cards in the current base set are included below.
    Energy is the printed cost before off-class surcharges. Card text and stats
    come directly from the game. Select an image to inspect the full card.</p>'''.format(count=len(cards))
    tokens = table(['Card', 'Created by', 'In the default deck?'], [
        ('Footsoldier', 'Commander, Rally and Banner.', 'Yes: four copies in Warrior.'),
        ('Ooze', 'Oozification, one per point of the destroyed minion’s current toughness.', 'No.'),
        ('Bubble', 'Bubble Shield. An attack on your hero triggers its bounce and destroys the Bubble.', 'No.'),
        ('Primordial', 'Summon Primordial creates a 10/10 after returning one targeted hero’s board to hand.', 'No. The spell has four copies in Mage.'),
        ('Burnout', 'Overwork creates it when destroyed. At the end of your turn it damages you for 2 and makes you discard a card.', 'No.')]) + '<p>These cards also belong to the base set and can be included in custom decks under the normal copy limits.</p>'
    tips = panels([
        ('Choose your opponent', 'At a multiplayer table, spending everything to eliminate one rival can leave you exposed to the others. Count damage across the whole table before committing.'),
        ('Build before buffing', 'Warrior buffs affect the minions already in play. Rally summons its Footsoldiers before adding power, so the new recruits benefit too.'),
        ('Plan your costs', 'A multiclass deck gains options but can lose tempo to the energy surcharge. Level-up trinkets help, and bounce or trinket removal can make those costs rise again.')])
    play = '''<p>Play in the browser on <a href="https://softmax.com/cards-and-casters">Softmax</a>, or run the native game from <code>games/cac</code> in a Polyworld checkout:</p>
    <pre class="guide-command"><code>nim c src/cac.nim
./cac --human
./cac --players 4 --human
./cac --cards</code></pre>
    <p>The human player picks a class and uses its preconstructed deck. Pass
    <code>--human players/archer_warrior.bas</code> to use that script’s class and
    custom deck. Bots are BASIC scripts; recorded matches can be watched with
    <code>--replay PATH</code>.</p>'''
    sections = [
        section('overview', 'How to play', overview, 'champion'),
        section('classes', 'The three classes', classes, 'minion'),
        section('decks', 'Deckbuilding & multiclassing', decks, 'stats'),
        section('combat', 'Turns, combat & keywords', combat, 'attack'),
        section('levelups', 'Class level-ups', reference + levelups, 'mana')]
    for hero_class, key, icon in [('Archer', 'archer', 'range'), ('Warrior', 'warrior', 'damage'), ('Mage', 'mage', 'mana')]:
        sections.append(section(key, hero_class + ' cards', card_table([card for card in cards if card['heroClass'] == hero_class]), icon))
    sections += [section('tokens', 'Cards created by effects', tokens, 'minion'),
                 section('tips', 'Strategy notes', tips),
                 section('play', 'Play & write bots', play, 'champion')]
    visual = '''<img class="cac-wordmark" src="assets/cards-and-casters.svg" width="560" height="350" alt="Cards and Casters"><img class="cac-loading-art" src="assets/moonlit-table.webp" width="1672" height="941" alt="An archer, warrior and mage playing cards in a moonlit observatory">'''
    write_guide('AWM', 'Cards and Casters', 'Card game · 2–7 heroes · Custom decks',
        'Build a deck, choose your targets and outlast the table. A duel or multiplayer card battle with Archers, Warriors, Mages and room to mix all three.',
        'cards-and-casters.svg', [('Players', '2–7'), ('Starting life', str(data['startingLife'])),
        ('Deck size', f"{data['deckSize']} cards"), ('Opening hand', f"{data['openingHand']} cards")],
        sections, [('Game rules & bot guide', CAC_SOURCE + 'README.md'),
        ('Card definitions & preconstructed decks', CAC_SOURCE + 'src/baseset.nim'),
        ('Turn, combat & victory rules', CAC_SOURCE + 'src/core/sim.nim'),
        ('Deck validation', CAC_SOURCE + 'src/core/cardset.nim'),
        ('Exported card data', 'assets/cards.json')], '#e2c597', reviewed='9 November 2026',
        stylesheet='guide.css', body_class='cac-guide', hero_visual=visual)



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
        ('AWM', 'Cards and Casters', 'AWM/assets/cards-and-casters.svg',
         'Build a deck, explore all 39 cards, and outlast a table of up to seven heroes.', False),
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
  <meta name="description" content="Game guides for Gods of the Arena, Light vs Dark, Call to Adventure, Heartleaf, Cards and Casters, Pudge Wars, and Paintbot PW.">
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
