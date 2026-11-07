Source: [Polyworld Buff](https://softmax-universe.github.io/polyworld-buff/CTA/). Synced snapshot; interactive views remain on the source site.

![Call to Adventure](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_199a7856-1519-4058-a40f-817caf116549.png)

A fighter, a wizard, a rogue, and a cleric descend a seeded dungeon. They start with empty bags. Kill monsters for gold and gear, pick the piles up off the floor, then climb back to the surface before the vault's reinforcements close the way out.

| Stat | Value |
| --- | --- |
| HEROES | 4 |
| LEVELS | 6 |
| ITEM SLOTS | 2 |
| DROPS | 22 |
| MINUTES | 20 |

THE RUN

## How the dungeon works

Call to Adventure is a deterministic four-hero expedition. The map is six stacked 128×128 slabs: Surface, Old Halls, Caves, Flooded Deep, Lava Hall, and the Vault. Ramps link the floors. One BASIC script drives each hero.

The party starts on the surface with no items and fights down. When the vault is empty they turn around. On the climb, monsters respawn on floors above them every 15 seconds. Every kill drops gold. Deeper floors, and golems, can also drop a usable item. Gold goes into that hero's purse, not a shared pot. Gear fills one of two item slots. A hero banks gold only after reaching the surface. If everyone dies, the run is lost. If time runs out, the match ends wherever they stand.

Each class has four abilities (keys 1–4) and two item slots (Q, E). Click a pile or item on the floor to pick it up. Click an item slot or press Q or E to use it. Right-click a slot or hold Shift and press Q or E to drop it. Clicking an enemy paints it with a red outline. Damage rolls **base + 0..spread** , then a class power percent. Healing is negative damage and skips that percent.

| Reference | Details |
| --- | --- |
| Regen | 4% max HP every 0.5s after 3s idle |
| Encumbrance | Speed 100 / 85 / 70 / 50% |
| Guard | Guarded targets take 40% damage |
| Aggro | 11 tiles, then hunt the floor |
| Cap | 90 monsters in the whole dungeon |
| Clock | 24 ticks a second, 20 minute run |

THE PARTY

## Heroes and ability bars

Speed is in tiles per second. Power is the percent applied to strike damage. Items is the two-slot bag. Light is vision radius in tiles.

![Brom](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_b4c24532-fb27-4dec-8749-dd7f54603209.png)

BROM · FIGHTER

### FRONTLINE

| Stat | Value |
| --- | --- |
| HP | 340 |
| MANA | 0 |
| POWER | 150% |
| SPEED | 2.50 |
| ITEMS | 2 |
| LIGHT | 6 |

| Key | Ability | Details |
| --- | --- | --- |
| 1 | Firebrand Sword | PRIMARY · 14–20 DMG · 21–30 HIT · 1 TILE · NO CD |
| 2 | Molten Fist | 34–44 DMG · 51–66 HIT · 1 TILE · 5s CD |
| 3 | Lion Guard | SELF · 2s CD · NO MANA |
| 4 | Blazing Blade | 28–36 DMG · 42–54 HIT · 1 TILE · 4s CD |

![Nyra](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_0b121a40-a5bc-46cf-bf7a-199baddcf4a6.png)

NYRA · WIZARD

### BURST MAGE

| Stat | Value |
| --- | --- |
| HP | 200 |
| MANA | 160 |
| POWER | 125% |
| SPEED | 2.60 |
| ITEMS | 2 |
| LIGHT | 8 |

| Key | Ability | Details |
| --- | --- | --- |
| 1 | Meteor Strike | PRIMARY · 22–30 DMG · 27–37 HIT · 12 MANA · 7 TILES · 1.5s CD |
| 2 | Frost Lance | 10–14 DMG · 12–17 HIT · 16 MANA · 5 TILES · 4s CD |
| 3 | Void Portal | 20 MANA · 4 TILES · 10s CD |
| 4 | Lightning Storm | 30–40 DMG · 37–50 HIT · 18 MANA · 6 TILES · 2s CD |

![Fenn](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_e3badbf5-417b-4af6-b50b-041f07eaeeee.png)

FENN · ROGUE

### MOBILE STRIKER

| Stat | Value |
| --- | --- |
| HP | 250 |
| MANA | 40 |
| POWER | 135% |
| SPEED | 3.40 |
| ITEMS | 2 |
| LIGHT | 5 |

| Key | Ability | Details |
| --- | --- | --- |
| 1 | Venom Dagger | PRIMARY · 12–16 DMG · 16–21 HIT · 1 TILE · 4s CD |
| 2 | Verdant Arrow | 9–14 DMG · 12–18 HIT · 6 TILES · 1s CD |
| 3 | Shadow Cloak | SELF · 15s CD |
| 4 | Gale Slash | 20–26 DMG · 27–35 HIT · 1 TILE · 2s CD |

![Zyra](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_118d62c4-33df-47e6-9a82-4552323bf0bb.png)

ZYRA · CLERIC

### SUPPORT

| Stat | Value |
| --- | --- |
| HP | 270 |
| MANA | 180 |
| POWER | 100% |
| SPEED | 2.70 |
| ITEMS | 2 |
| LIGHT | 6 |

| Key | Ability | Details |
| --- | --- | --- |
| 1 | Solar Hammer | PRIMARY · 14–20 DMG · 1 TILE · NO CD |
| 2 | Healing Bloom | HEAL 70 · 18 MANA · 4 TILES · 3s CD |
| 3 | Angelic Emblem | 24 MANA · 4 TILES · 15s CD |
| 4 | Sun Orb | 26–36 DMG · 20 MANA · 5 TILES · 10s CD |

THE DUNGEON

## Monsters

Surface has no spawns. Deeper floors mix nastier species and add 10% hit points per level. Monsters swing Firebrand Sword at their own power percent, so they lose a straight damage race against the party.

![Skeleton](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_c3a6e56a-5eb8-4c61-a392-02bd199b4df3.png)

### Skeleton

OLD HALLS

60 HP base. Speed 2.20. Sight 6. Power 55%.

![Orc](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_d9fbd6c7-bd38-451b-9dc7-8a595777bd1f.png)

### Orc

CAVES

90 HP base. Speed 3.00. Sight 9. Power 70%.

![Lich](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_b28fd0ad-61b3-4e74-b6f7-730eb8373196.png)

### Lich

FLOODED DEEP

130 HP base. Speed 2.00. Sight 10. Power 80%.

![Golem](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_1c4fbe98-5fed-43ce-86fe-04411c39646f.png)

### Golem

LAVA / VAULT

260 HP base. Speed 1.40. Sight 5. Power 110%. Often drops a usable item.

THE HAUL

## Monster drops

Items are not attached to heroes. The four abilities on each bar are the class kit. Q and E start empty. Every drop lands on the monster's tile. A hero holds gear only after they pick it up, and they can drop it again. Every drop has a gold value. Treasure is gold only and goes straight into that hero's purse. The old per-hero extras (four from each class bar) are now shared drops. Any hero can use any of them. A fighter gets little from a mana potion, and a wizard still swings a flail if they pick one up.

Every kill leaves a gold pile. Deeper floors, and golems, can also drop one extra item from the table below. Click the pile or the item to pick it up. Right-click a slot, or hold Shift and press Q or E, to drop gear back on the floor. Each hero keeps their own gold. It only counts as banked after that hero walks it onto the surface.

| Reference | Details |
| --- | --- |
| Not on the kit | Heroes spawn with empty Q / E slots |
| On the tile | Drops land on the monster's floor tile |
| After pickup | A hero holds an item only once they take it |
| Can drop | Shift+Q / Shift+E or right-click the slot |

### Gold value

![Gold pile](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_e9afc816-1b84-47b2-a222-0464c83661d8.png)

### Gold Pile

12+

Always dropped. Purse only. Value is 12 plus 8 per floor.

![Gemstone](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_91eb4428-6c22-4df0-8961-a1d4303c29e4.png)

### Gemstone

60

Purse only. Common extra drop on the upper floors.

![Chalice](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_94d13ce6-6723-42a5-a2e5-7be7d47f2747.png)

### Chalice

140

Purse only. Starts showing up in the flooded deep.

![Idol](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_b6626dc8-5895-43e0-bd20-5db0a922eada.png)

### Idol

300

Purse only. Lava, vault, and golem extra drop.

![Crown](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_e763491b-6b21-40a6-8b00-fd1361e419fa.png)

### Crown

900

Purse only. Vault prize. Golems can roll it too.

### Usable by every hero

![Healing potion](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_3ab033de-96d9-41a5-b00d-4ef44463e51d.png)

### Healing Potion

40

Consumable. Cleric extra. Heals 80.

![Fire phoenix](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_c5847716-12af-4e94-9aee-d54557ec9db7.png)

### Fire Phoenix

100

Cooldown. Cleric extra. Heals 90 on use.

![Nature talisman](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_6a28ec71-4bd1-42d9-a713-4ad60f60d875.png)

### Nature Talisman

85

Cooldown. Cleric extra. Heals 40 and restores 30 mana.

![Cosmic flare](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_4a902ab7-5d83-49b6-aa31-1fdd3b28b404.png)

### Cosmic Flare

95

Cooldown. Cleric extra. 24–32 damage at 6 tiles.

![Iron flail](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_8b21f61e-cae7-4e34-9828-ca7e4e433404.png)

### Iron Flail

70

Cooldown. Fighter extra. 18–26 damage at 2 tiles.

![Inferno aegis](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_caa15265-87d8-440e-bbf9-801ae0fdd76e.png)

### Inferno Aegis

75

Cooldown. Fighter extra. Self guard for 2.7s.

![Winged boot](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_a5ba494f-b221-41b6-af4b-332be25a65d0.png)

### Winged Boot

100

Cooldown. Fighter extra. 130% move speed for 3s.

![Blazing blade](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_c9cada48-3ed4-4ee6-bf30-556f354ac883.png)

### Blazing Blade

90

Cooldown. Fighter extra. 28–36 damage at 1 tile.

![Ice wall](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_f3df7785-63db-43ff-9a5f-f37dddbe1618.png)

### Ice Wall

70

Cooldown. Wizard extra. Self guard. No mana needed as an item.

![Lightning storm](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_d4e65b8d-14d0-42e8-a186-32f26601984a.png)

### Lightning Storm

110

Cooldown. Wizard extra. 30–40 damage at 6 tiles.

![Mana potion](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_96313496-0146-4d6d-aedd-0bfed40b9884.png)

### Mana Crystal

45

Consumable. Wizard extra. Restores 50 mana. Useless to Brom.

![Arcane meteor](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_0a226e45-56cd-48de-8486-094a6d6bbf72.png)

### Arcane Meteor

120

Cooldown. Wizard extra. 36–48 damage at 8 tiles.

![Void blade](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_00dd8b5f-afca-4e8c-93e1-015dda05af93.png)

### Void Blade

80

Cooldown. Rogue extra. 16–21 damage at 1 tile.

![Shadow comet](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_3d34f2ed-eae4-45c1-b84b-96b2869c0eff.png)

### Shadow Comet

85

Cooldown. Rogue extra. 14–20 damage at 7 tiles.

![Gale slash](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_288f4743-24f5-44b0-a761-c258e6b1c4be.png)

### Gale Slash

90

Cooldown. Rogue extra. 20–26 damage at 1 tile.

![Thorn ring](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_70527495-d8ff-497f-b22b-fca5370ac0a5.png)

### Thorn Ring

70

Cooldown. Rogue extra. Self guard.

![Battle horn](https://softmax-public.s3.amazonaws.com/post-media/user/s25q6tn121cx1j3z7ql3ga5d/media_b5c4399d-0453-4ed5-9ce0-acb0e1b38453.png)

### Battle Horn

80

Cooldown. Shared extra. Guards nearby allies for 2s.

Numbers come from `examples/call_to_adventure/content.nim`, `ui.nim`, and `sim.nim`. Artwork is bundled with this guide.

[Read the Softmax wiki](https://softmax.com/call-to-adventure/wiki/game-guide) · [All games](https://softmax-universe.github.io/polyworld-buff/)


---

Synced from Polyworld Buff by Codex.
