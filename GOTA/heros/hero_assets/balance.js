(() => {
  'use strict';
  const report = JSON.parse(document.getElementById('balance-data').textContent);
  const catalog = JSON.parse(document.getElementById('report-data').textContent).catalog;
  const root = document.getElementById('balance-report');
  const n = (value, digits = 0) => Number(value).toLocaleString('en-US', {
    minimumFractionDigits: digits, maximumFractionDigits: digits
  });
  const pct = value => value == null ? '—' : n(value * 100, 1) + '%';
  const date = value => new Date(value).toLocaleString('en-US', {
    timeZone: 'America/Los_Angeles', timeZoneName: 'short'
  });
  const colors = {FL: 'var(--blue)', F: 'var(--red)', M: 'var(--xp)', S: 'var(--green)', C: 'var(--gold)'};
  const roles = {FL: 'Frontline', F: 'Fighter', M: 'Mage', S: 'Support', C: 'Carry'};
  const link = name => '#hero=' + catalog[name].slug;
  const label = row => `<a href="${link(row.hero)}">${row.hero} <span class="balance-role-${row.role}">(${row.role})</span></a>`;
  const decisive = report.games - (report.outcomes.time_limit || 0);
  const timeout = report.outcomes.time_limit || 0;
  const topThree = report.heroes.slice(0, 3);
  const sparse = report.heroes.filter(row => row.decisive_picks < 20);
  const unchosen = report.heroes.filter(row => row.manual_picks === 0);
  const role = code => report.roles.find(row => row.role === code);
  const heroStats = name => report.heroes.find(row => row.hero === name);
  const fact = (value, title, sub) => `<div class="fact"><div><b>${value}</b><span class="label">${title}</span><br><small>${sub}</small></div></div>`;
  root.innerHTML = `
    <div class="section-title"><h2>Recent balance snapshot</h2><span class="label">Main ladder · Release ${report.release}</span></div>
    <p class="balance-caption">${date(report.start)} – ${date(report.end)} · Current release only.</p>
    <div class="facts">
      ${fact(n(report.games), 'Verified games', 'Rounds ' + report.first_round + '–' + report.last_round)}
      ${fact(n(report.players), 'Players', 'Mixed policies in each team')}
      ${fact(n(report.policies), 'Policy versions', 'Repeated across the window')}
      ${fact(n(report.appearances), 'Hero picks', n(report.auto_picks) + ' draft-timeout picks')}
    </div>
    <div class="insight"><p><b>${pct(timeout / report.games)} of games reached the time limit.</b> ${n(decisive)} games produced a winner. Hero win rates below describe this ladder sample; they do not isolate hero strength from policy skill or team composition.</p></div>
    <div class="balance-grid">
      <article class="panel pad"><h2>Match outcomes</h2>
        <div class="outcomes balance-outcomes" aria-label="${report.outcomes.BlueTeam || 0} blue wins, ${report.outcomes.RedTeam || 0} red wins, ${timeout} timeouts">
          <i class="blue-win" style="width:${(report.outcomes.BlueTeam || 0) / report.games * 100}%"></i>
          <i class="red-win" style="width:${(report.outcomes.RedTeam || 0) / report.games * 100}%"></i>
          <i class="timeout" style="width:${timeout / report.games * 100}%"></i>
        </div>
        <div class="legend"><span><b class="blue">${n(report.outcomes.BlueTeam || 0)}</b> blue wins</span><span><b class="red">${n(report.outcomes.RedTeam || 0)}</b> red wins</span><span><b>${n(timeout)}</b> time-limit draws</span></div>
        <div class="metric-grid">
          <div class="metric"><span class="label">Battle time limit</span><b>${report.battle_caps.map(value => n(value)).join(' / ')} min</b><small>Read from each replay configuration</small></div>
          <div class="metric"><span class="label">Average battle</span><b>${n(report.avg_battle_minutes, 2)} min</b><small>Draft time excluded; median ${n(report.median_battle_minutes, 1)} min</small></div>
          <div class="metric"><span class="label">Decisive games</span><b>${n(report.avg_decisive_minutes, 2)} min</b><small>Average time to finish a winning battle</small></div>
          <div class="metric"><span class="label">Blue share of wins</span><b>${pct((report.outcomes.BlueTeam || 0) / decisive)}</b><small>Among ${n(decisive)} decisive games</small></div>
        </div>
        <p class="balance-caption">The recorded battle caps are ${report.battle_caps.map(value => n(value)).join(" / ")} minutes. Duration in the hero performance table includes the draft, matching the game's score denominator.</p>
      </article>
      <article class="panel pad"><h2>What people are picking</h2>
        <p>${topThree.map(row => row.hero).join(', ')} account for <b class="gold">${pct(topThree.reduce((sum, row) => sum + row.seat_share, 0))}</b> of all seats.</p>
        <div id="balance-pick-chart"></div>
        <p class="balance-caption">Share of ${n(report.appearances)} seats. Duplicate heroes count separately. Colors indicate roles. FL Frontline · F Fighter · M Mage · S Support · C Carry.</p>
      </article>
    </div>
    <div class="section-title"><h2>Hero picks & results</h2><span class="label">Ordered by popularity</span></div>
    <div class="panel"><div class="scroll"><table>
      <thead><tr><th>Hero / role</th><th>Picks</th><th>Seat share</th><th>Game presence</th><th>Chosen / auto</th><th>W / L / D</th><th>All-pick win rate</th><th>Decisive win rate</th><th>Decisive picks</th><th>Policy versions</th></tr></thead>
      <tbody>${report.heroes.map(row => `<tr><td>${label(row)}</td><td>${n(row.picks)}</td><td>${pct(row.seat_share)}</td><td>${pct(row.game_presence)}</td><td>${n(row.manual_picks)} / ${n(row.auto_picks)}</td><td>${n(row.wins)} / ${n(row.losses)} / ${n(row.draws)}</td><td>${pct(row.win_rate)}</td><td class="${row.decisive_picks < 20 ? 'balance-low' : 'gold'}">${pct(row.decisive_rate)}</td><td>${n(row.decisive_picks)}${row.decisive_picks < 20 ? ' · sparse' : ''}</td><td>${row.policies}</td></tr>`).join('')}</tbody>
    </table></div><div class="table-note">Chosen = accepted pick commands. Auto = heroes selected by the engine after a draft timeout. Seat share = picks / all seats. Game presence = games containing that hero / all games. All-pick win rate counts draws as non-wins; decisive win rate = wins / (wins + losses). Decisive picks are appearances, not independent games. A mirrored or repeated hero can contribute both wins and losses in one match. “Sparse” flags fewer than 20 decisive appearances; it is a sample-size warning, not a significance test.</div></div>
    <div class="balance-grid">
      <article class="panel pad"><h2>How far heroes get</h2><p>Final progression by role, weighted by actual picks.</p>
        <div class="scroll"><table><thead><tr><th>Role</th><th>Mean level</th><th>Median</th><th>Level 12+</th><th>Level 18+</th><th>Mean XP</th></tr></thead>
          <tbody>${report.roles.map(row => `<tr><td class="balance-role-${row.role}">${roles[row.role]} (${row.role})</td><td>${n(row.avg_level, 2)}</td><td>${n(row.median_level, 1)}</td><td>${pct(row.level12)}</td><td>${pct(row.level18)}</td><td class="xp">${n(row.avg_xp)}</td></tr>`).join('')}</tbody>
        </table></div>
        <p class="balance-caption">Levels 12 and 18 are the second and third ultimate-rank gates, not evidence those ranks were purchased. XP is lifetime XP; winners also receive the existing 1,000 XP god-kill reward per hero. Equipment and learned builds vary.</p>
      </article>
      <article class="panel pad"><h2>Team composition</h2>
        <div class="metric-grid">
          <div class="metric"><span class="label">Duplicate heroes</span><b>${pct(report.duplicate_teams / (report.games * 2))}</b><small>Teams with a repeated hero</small></div>
          <div class="metric"><span class="label">All five roles</span><b>${pct(report.all_roles_teams / (report.games * 2))}</b><small>Teams with FL, F, M, S and C</small></div>
        </div>
        <p>${Object.entries(report.role_presence).map(([code, share]) => `<span class="balance-role-${code}">${code}</span> on ${pct(share)} of teams`).join(' · ')}</p>
        <div class="balance-lineups"><h3>Most common team lineups</h3>
          ${report.top_lineups.map(row => `<p><b>${n(row.teams)} teams</b> · ${row.heroes.join(' + ')}</p>`).join('')}
        </div><p class="balance-caption">Open Draft permits any hero and duplicates. These are observed choices, not composition requirements.</p>
      </article>
    </div>
    <div class="section-title"><h2>Farming & objective pressure</h2><span class="label">Verified death events</span></div>
    <div class="panel"><div class="scroll"><table><thead><tr><th>Hero / role</th><th>Creep last hits</th><th>Neutral kills</th><th>Buildings destroyed</th><th>Mirrored games</th><th>Top policy's pick share</th></tr></thead>
      <tbody>${report.heroes.map(row => `<tr><td>${label(row)}</td><td>${n(row.avg_last_hits, 1)}</td><td>${n(row.avg_neutral_kills, 1)}</td><td>${n(row.avg_buildings, 2)}</td><td>${n(row.mirror_games)}</td><td>${pct(row.top_policy_share)}</td></tr>`).join('')}</tbody>
    </table></div><div class="table-note">First three columns are final per-appearance averages. Buildings include towers and barracks credited to that hero; gods are excluded. Mirrored games have this hero on both teams. A hero dominated by one policy is especially hard to separate from that policy's skill.</div></div>
    <div class="section-title"><h2>Across the analysis window</h2><span class="label">Three equal groups of rounds</span></div>
    <div class="panel scroll"><table><thead><tr><th>Rounds</th><th>Games</th><th>Draw rate</th><th>Carry seat share</th><th>Carry mean final level</th></tr></thead><tbody>${report.trends.map(row => `<tr><td>${row.first_round}–${row.last_round}</td><td>${row.games}</td><td>${pct(row.draw_rate)}</td><td>${pct(row.carry_share)}</td><td>${n(row.carry_level, 2)}</td></tr>`).join('')}</tbody></table></div>
    <p class="balance-caption">All groups use the same balance release. Policy updates and matchups change over time, so this is descriptive, not a controlled before-and-after comparison.</p>
    <article class="panel pad balance-copy" style="margin-top:18px"><h2>What this says about balance</h2>
      <h3>Finishing games</h3><p>${n(timeout)} of ${n(report.games)} games timed out. Test objective pressure and bot finishing behavior before judging the patch from win rates alone. The observed faction split is ${report.outcomes.BlueTeam || 0} blue wins versus ${report.outcomes.RedTeam || 0} red wins; the faction split alone does not establish a side advantage.</p>
      <h3>Carry progression is still worth watching</h3><p>Carries finish at mean level <b>${n(role('C').avg_level, 2)}</b>; ${pct(role('C').level12)} reach level 12 and ${pct(role('C').level18)} reach level 18. These figures show how often their later progression is exercised. Tune and test the levels games actually reach before raising level-20 endpoints. This describes the combined Ranger/Crossbowman population and does not prove their early game is too weak.</p>
      <h3>Frontline survival and farming</h3><p>Frontline averages <b>${n(role('FL').avg_deaths, 1)} deaths</b> versus ${n(role('C').avg_deaths, 1)} for Carry and ${n(role('F').avg_deaths, 1)} for Fighter. Its mean final level is ${n(role('FL').avg_level, 2)}, versus ${n(role('C').avg_level, 2)} for Carry. Vanguard accounts for ${pct(heroStats('Vanguard Knight').picks / role('FL').picks)} of Frontline appearances. This suggests checking tank farming and positioning before adding another blanket health buff.</p>
      <h3>The two carries are not producing the same results</h3><p>Crossbowman averages ${n(heroStats('Crossbowman').avg_kills, 1)} hero kills and ${n(heroStats('Crossbowman').avg_buildings, 2)} buildings destroyed; Ranger averages ${n(heroStats('Ranger').avg_kills, 1)} kills and ${n(heroStats('Ranger').avg_buildings, 2)} buildings. Their similar progression curves do not produce equal ladder outcomes, but different policies and drafts prevent attributing the gap to the hero alone.</p>
      <h3>Pick coverage limits hero comparisons</h3><p>${sparse.length ? sparse.map(row => row.hero + ' (' + row.decisive_picks + ' decisive picks)').join(', ') + ' have particularly sparse decisive samples.' : 'Every hero has at least 20 decisive appearances in this snapshot.'} ${unchosen.length ? unchosen.map(row => row.hero).join(' and ') + ' had no deliberate picks; every appearance was a draft-timeout selection. Those heroes may be running policies designed for another class. ' : ''}Repeated policies, duplicate heroes and team results make even the larger counts correlated. Do not treat the highest raw rate as a hero tier list.</p>
      <h3>The reference draft has a selection bias</h3><p><a href="https://github.com/softmax-universe/polyworld/blob/2d38a1da94542b71f3a4824fa2939241c3087612/examples/gods_of_the_arena/players/base.bas#L17">base.bas</a> fills missing roles, then breaks equal-score ties by hero order. That favors Vanguard, Ranger, Arcanist, Druid and Demon Hunter over their same-role alternatives. Policies that reuse this draft can inherit that preference. This is a possible contributor to the pick skew; submitted policy implementations were not audited here.</p>
      <h3>Next useful balance test</h3><p>Use the same policy across a shuffled roster with one of each role per team. Compare finishing rate, carry survival and level timing, frontline deaths, and damage to objectives. Repeat with exchanged team sides and fixed map seeds. Keep this current-ladder snapshot separate from those controlled tests.</p>
    </article>
    <div class="balance-note"><p><b>Evidence:</b> all ${n(report.games)} replay simulations matched every recorded hash across ${n(report.verified_ticks)} ticks and all hosted seat scores. Completed games only, on release ${report.release} / gameplay ${report.replay_version}. This overview covers the current release within the dated window. The hero performance table also includes any earlier releases in that window, with a release filter for comparison. Main Gods of the Arena ladder only; the student league is outside this report. <a href="${report.source}">View the main ladder</a>.</p></div>`;

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 590 335');
  svg.setAttribute('class', 'balance-picks');
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', 'Hero pick shares, ordered by popularity');
  document.getElementById('balance-pick-chart').append(svg);
  const add = (parent, tag, attributes, text = '') => {
    const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
    node.textContent = text;
    parent.append(node);
    return node;
  };
  const maximum = report.heroes[0].seat_share;
  report.heroes.forEach((row, i) => {
    const y = i * 33 + 15;
    const anchor = add(svg, 'a', {href: link(row.hero)});
    add(anchor, 'text', {x: 0, y, class: 'pick-name'}, row.hero + ' (' + row.role + ')');
    add(anchor, 'title', {}, row.picks + ' picks; ' + pct(row.seat_share) + ' of seats');
    add(svg, 'rect', {x: 175, y: y - 11, width: 320, height: 15, rx: 3, class: 'pick-track'});
    add(svg, 'rect', {x: 175, y: y - 11, width: row.seat_share / maximum * 320, height: 15, rx: 3, fill: colors[row.role]});
    add(svg, 'text', {x: 585, y, 'text-anchor': 'end'}, pct(row.seat_share));
  });

  function show() {
    const slug = new URLSearchParams(location.hash.slice(1)).get('hero');
    const hero = Object.values(catalog).find(row => row.slug === slug);
    root.hidden = !!hero;
    if (!hero) return;
    const row = report.heroes.find(row => row.hero === hero.name);
    const panel = document.getElementById('hero-panel');
    if (!row || !panel || panel.querySelector('.balance-profile')) return;
    const note = document.createElement('div');
    note.className = 'balance-note balance-profile';
    note.innerHTML = `<p><b>${n(row.picks)} picks (${pct(row.seat_share)} of seats).</b> Decisive win rate: ${pct(row.decisive_rate)} across ${n(row.decisive_picks)} appearances (${row.wins} wins / ${row.losses} losses). ${n(row.draws)} draws. ${row.decisive_picks < 20 ? 'Decisive sample is sparse. ' : ''}These appearances include repeated or mirrored heroes and are not independent games.</p>`;
    panel.prepend(note);
  }
  window.addEventListener('hashchange', show);
  document.getElementById('version').addEventListener('change', show);
  show();
})();
