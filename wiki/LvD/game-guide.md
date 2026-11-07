Source: [Polyworld Buff](https://softmax-universe.github.io/polyworld-buff/LvD/). Synced snapshot; interactive views remain on the source site.

![Light vs Dark](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_7b17db9a-f007-4fa0-9c9c-82d92d445e76.png)

A 1v1 real-time strategy match on a 128-tile map that is fair by construction: Dark's half is Light's half rotated 180 degrees. Two BASIC overlords gather gold and wood, raise an army, and try to wipe the other side out.

| Stat | Value |
| --- | --- |
| UNIT KINDS | 8 |
| BUILDINGS | 8 |
| STARTING GOLD | 800 |
| STARTING WOOD | 400 |
| FOOD CAP | 100 |

THE MATCH

## How a game is won

Each side starts with a town hall, five peasants or peons, 800 gold, and 400 wood. Neutral gold mines sit on the map. Trees give four wood trips then vanish. Food comes from the hall and farms, capped at 100. Army size is also capped at 100 living units.

Combat is piercing plus basic, then armor. Piercing always lands. Basic is reduced by armor and never goes below zero. Most swings miss 20% of the time. Catapults never miss, deal 255 piercing, and splash 63 piercing onto king-move neighbours.

A player is defeated when they have no standing buildings and no peon left to raise one. If the 20-minute clock hits first, score is buildings × 1000, plus army × 100, plus gold and wood ever gathered ÷ 100.

| Reference | Details |
| --- | --- |
| Gold trip | 100 gold, 2.5s in the mine, 4 miners |
| Wood trip | 100 wood, 3.3s chop, 400 per tree |
| Hall / farm | +5 and +4 food |
| Walk | Infantry 10 ticks/tile, siege 16 |
| Tower | 12 damage, 6 range, 1s cooldown |
| Clock | 24 ticks a second, fog of war |

THE ARMIES

## Units

Light and Dark share gold, wood, train time, and most combat numbers. Where they differ, both portraits and both rows are shown. Damage is piercing / basic. Speed is ticks to cross one tile.

![Peasant](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_60ab024b-da61-4647-8613-7b5d786d48aa.png)

![Peon](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_636bf265-45b2-43a5-99a6-fda738f1053b.png)

LIGHT PEASANT

DARK PEON

### Worker

Town hall · 400 gold · 18.8s

| Stat | Value |
| --- | --- |
| HP | 40 |
| ARMOR | 0 |
| DMG | 0 / 1 |
| RANGE | 1 |
| STEP | 10 |
| SIGHT | 5 |

![Footman](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_0f64fe61-50c5-42e8-84de-194a81199790.png)

![Grunt](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_9bdbfd44-83ef-4b6a-977d-aa334f8dfc7a.png)

LIGHT FOOTMAN

DARK GRUNT

### Soldier

Barracks · 400 gold · 15s

| Stat | Value |
| --- | --- |
| HP | 60 |
| ARMOR | 2 |
| DMG | 1 / 9 |
| RANGE | 1 |
| STEP | 10 |
| SIGHT | 5 |

![Archer](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_061e6205-217c-40ec-a0e9-867d27f2ea38.png)

![Spearman](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_cf09a5b1-72c0-42e2-93da-6fe3f0bafd2c.png)

LIGHT ARCHER

DARK SPEARMAN

### Ranged

Barracks · mill · 450g 50w · 17.5s

| Stat | Value |
| --- | --- |
| HP | 60 |
| ARMOR | 1 |
| DMG | 4–5 / 0 |
| RANGE | 5 / 4 |
| STEP | 10 |
| SIGHT | 7 |

Light: 4 piercing, 5 range. Dark: 5 piercing, 4 range. Cooldown 1.5s.

![Conjurer](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_ba988530-81cd-417e-88db-e896eb4972fb.png)

![Warlock](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_d0a355a8-af54-42d9-a0f0-23abac4f34fe.png)

LIGHT CONJURER

DARK WARLOCK

### Mage

Tower · 900 gold · 22.5s

| Stat | Value |
| --- | --- |
| HP | 40 |
| ARMOR | 0 |
| DMG | 6 / 0 |
| RANGE | 3 / 2 |
| STEP | 10 |
| SIGHT | 7 |

Light range 3. Dark range 2. Cooldown 1.5s.

![Knight](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_0ae4d220-9541-4fc3-a1f3-480e943ae5de.png)

![Raider](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_0116a04e-449f-434b-a179-057f6359a526.png)

LIGHT KNIGHT

DARK RAIDER

### Cavalry

Barracks · stables + smith · 850g · 20s

| Stat | Value |
| --- | --- |
| HP | 90 |
| ARMOR | 5 |
| DMG | 1 / 13 |
| RANGE | 1 |
| STEP | 10 |
| SIGHT | 6 |

![Catapult](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_ba9e40cd-52e6-40ba-8980-1a0cc769729c.png)

![Catapult](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_4da5e8fb-5871-4694-8f56-b5df7ab10380.png)

LIGHT CATAPULT

DARK CATAPULT

### Siege

Barracks · smith + mill · 900g 200w · 25s

| Stat | Value |
| --- | --- |
| HP | 120 |
| ARMOR | 0 |
| DMG | 255 / 0 |
| RANGE | 8 |
| STEP | 16 |
| SIGHT | 8 |

Never misses. 63 splash piercing. 8s cooldown.

![Cleric](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_b2f8a2d8-21c1-40f9-b9dd-9bfa244dcb47.png)

![Necrolyte](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_b28fd0ad-61b3-4e74-b6f7-730eb8373196.png)

LIGHT CLERIC

DARK NECROLYTE

### Support

Church / temple · 700 gold · 20s

| Stat | Value |
| --- | --- |
| HP | 40 |
| ARMOR | 0 |
| DMG | 6 / 0 |
| RANGE | 1 / 2 |
| STEP | 10 |
| SIGHT | 7 |

Light range 1. Dark range 2. Cooldown 2s.

![Elemental](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_1c4fbe98-5fed-43ce-86fe-04411c39646f.png)

![Daemon](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_832bc995-c4fd-4ee9-9394-08524d163aa4.png)

LIGHT ELEMENTAL

DARK DAEMON

### Summon

Tower · 1200 gold · 30s

| Stat | Value |
| --- | --- |
| HP | 250 / 300 |
| ARMOR | 0 |
| DMG | 40 / 65 |
| RANGE | 3 / 1 |
| STEP | 10 |
| SIGHT | 6 |

Light: 250 HP, 40 piercing, range 3. Dark: 300 HP, 65 basic, range 1.

THE TOWN

## Buildings

Same costs and hit points on both sides. Dark names stables as kennels and church as temple. Gold mines are neutral, 25,000 on the main and 15,000 on expansions.

![Town hall](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_c5cd0be1-7ce2-46f1-8ba8-ea3c6298a205.png)

### Town Hall

1200   800

1200 HP. 30s. 3×3. +5 food. Gold and wood drop-off. Trains workers.

![Light hall](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_c5cd0be1-7ce2-46f1-8ba8-ea3c6298a205.png)

![Dark hall](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_23d7a011-b940-4f69-9679-ea18e72521d5.png)

![Farm](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_e59990a9-4ac5-44ff-b6de-16b61e2d913d.png)

### Farm

400   200

400 HP. 10s. 2×2. +4 food.

![Barracks](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_eab1e306-dcfa-4025-bb15-2c24bf61e2c1.png)

### Barracks

600   400

800 HP. 20s. 3×3. Trains soldiers, ranged, knights, siege.

![Light barracks](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_eab1e306-dcfa-4025-bb15-2c24bf61e2c1.png)

![Dark barracks](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_1ed29a0b-1e81-41d2-b399-b00de418c0b8.png)

![Lumber mill](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_1bb9171d-82b9-41c1-8e4b-a8acefa03229.png)

### Lumber Mill

500   300

600 HP. 15s. 3×3. Wood drop-off. Unlocks ranged and towers.

![Tower](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_0f6fe2ae-d3b3-457c-a0ec-c4b85545eda7.png)

### Tower

500   300

700 HP. 15s. 2×2. Needs mill. 12 damage, 6 range, sight 9. Trains mages and summons.

![Stables](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_7da3c8fd-ae7e-4221-b1fc-93da2c91a525.png)

### Stables / Kennels

600   400

700 HP. 20s. 3×3. Needs barracks. Unlocks cavalry with the smith.

![Church](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_66736bbd-65ec-4f2b-82f5-c083c952e9ad.png)

### Church / Temple

700   400

700 HP. 20s. 3×3. Needs barracks. Trains cleric / necrolyte.

![Blacksmith](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_2e767e8d-d48e-4aaf-8d5d-0ebe9472b885.png)

### Blacksmith

600   400

700 HP. 15s. 3×3. Needs barracks. Unlocks knights and catapults.

![Gold mine](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_1105a562-9904-434f-a8fa-09f0832b449c.png)

### Gold Mine

Neutral

2000 HP. 2×2. Main 25,000 gold. Expansion 15,000. Four miners at a time.

Numbers come from `examples/light_vs_dark/content.nim` and `ui.nim`. Artwork is bundled with this guide.

[Read the Softmax wiki](https://softmax.com/light-vs-dark/wiki/game-guide) · [All games](https://softmax-universe.github.io/polyworld-buff/)


---

Synced from Polyworld Buff by Codex.
