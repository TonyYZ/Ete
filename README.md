# Ítí (Ete) — An Artistic Constructed Language and Visual Script

Ítí is an artistic constructed language with a generative visual writing system. Text is not laid out in a grid of discrete glyphs but rendered as a continuous path: consonants are drawn as distinct strokes along a flowing line, vowels encode prosodic and morphological information (accent, layer, branching), and multi-branch structures called *fuseaux* create forking paths that rejoin. The project includes a Python renderer that takes Ítí text as input and produces either an interactive turtle-graphics display or an exported SVG file. A collision-avoidance system in maze mode ensures that strokes never cross each other, producing output that resembles a space-filling curve constrained by linguistic structure. The name *ítí* means "language" or "word" in the language itself.

---

## Motivation

Ítí explores whether a writing system can encode phonological and morphological structure spatially — making the hierarchical organisation of a word visible in the geometry of its rendered form — while remaining legible as a continuous path rather than a sequence of disconnected symbols. The project also functions as a learnability experiment: can learners acquire an unfamiliar but structurally motivated writing system more readily than an arbitrary one?

---

## Language Overview

### Consonants

Consonants are the primary carriers of meaning. Each consonant maps to a specific visual stroke. Consonants are divided into two direction classes:

| Class | Consonants | Visual behaviour |
|-------|-----------|-----------------|
| **Passive** (horizontal strokes) | ṡ s b d n v r g h `-` | drawn perpendicular to the current direction of travel |
| **Active** (vertical strokes) | ż z p t m f l c ċ `\|` | drawn along the current direction of travel |
| **Neutral** | y w | adapt to the current direction |

The distinction between passive and active consonants governs how the drawing direction alternates as text is rendered, creating the characteristic serpentine path of the script.

### Vowels and prosody

Vowels appear between consonants and encode three kinds of information, none of which produce visible strokes of their own:

- **Accent** — the number of acute marks (`á é í ó ú`) on a vowel determines how many dot markers are placed beside the subsequent consonant stroke.
- **Layer** — the vowel class (`i`-type vs. `u`-type vs. `a`-type) encodes a morphological layer that determines the orientation of loop ornaments added to consonant strokes.
- **Branching** — sequences of vowels flanking a consonant cluster with a special separator (`ơ`, `ớ`, front/back vowel pairs) trigger *fuseaux*: the rendering splits into two or more parallel paths that proceed side by side before rejoining.

### Fuseaux

A *fuseau* (French: spindle) is the core grammatical and visual structure of Ítí. Three patterns are recognised by the parser:

| Pattern | Notation | Meaning |
|---------|----------|---------|
| **Simple fuseau** | `C₁ ơ C₂` | two branches, no flanking vowels |
| **Dual fuseau** | `[e]·C₁ C₂·[o]` | two branches with optional front/back vowel frame |
| **Complex fuseau** | `[e]·C₁ [ớ/e·C·o]+·C₂ [o]` | two or more inner branches between outer branches |

Inner fuseaux can be nested inside outer fuseaux, creating recursive branching structures. The parser resolves ambiguities between fuseau types by trying each pattern in order and backtracking on failure.

### Example text

```
Ưrah rơm, izucun. Ucunizaṡ, ĩhemõṡũl. Itaé gớt, izupun.
```

The text in `ItiDrawer.py` is a prose passage in Ítí demonstrating all major grammatical and visual features of the script, including nested fuseaux, layered ornaments, and sentence-final markers.

---

## Files

| File | Description |
|------|-------------|
| `ItiParser.py` | Parses Ítí text into structured branch trees consumed by the renderer |
| `ItiDrawer.py` | Renders parsed trees as a continuous visual path using Python turtle graphics |
| `Iti2IPA.py` | Converts Ítí orthography to IPA (dependency of ItiParser) |

---

## Pipeline

```
Ítí text  →  ItiParser.read()  →  branch trees  →  ItiDrawer.draw()  →  screen / SVG
```

**ItiParser** proceeds in two stages:

1. **Split** — the text is divided into clauses at punctuation boundaries.
2. **Parse** — each clause is scanned left-to-right with a recursive regex parser. The parser tries, in order, to identify simple fuseaux, dual fuseaux, and complex fuseaux; falling back to flat consonant-by-consonant parsing for non-branching sequences. Output is a nested list structure where each node is either a consonant element `[char, accent, layer]` or a branching structure (list of branches).

**ItiDrawer** proceeds in three stages for each fuseau:

1. **allocLength** — computes how much horizontal (or vertical) space each branch of a fuseau needs along the direction of travel.
2. **allocWidth** — computes how much perpendicular space each branch needs, to prevent overlap between adjacent branches.
3. **drawFuseau** — walks through the branches in order, drawing each consonant stroke using Python's turtle module, stepping sideways between branches according to the pre-computed widths.

In **maze mode**, before committing any stroke to the canvas, the renderer tests each bounding box against a quad-tree (`pyqtree`) of all previously drawn regions. On collision, it backtracks (using turtle's undo buffer) and tries an alternative orientation. If all alternatives are exhausted, it retraces further up the drawing history. This guarantees that the final output is a non-self-intersecting path.

---

## Usage

### Basic rendering

```python
from ItiParser import read
from ItiDrawer import draw
from turtle import Screen, Turtle

txt = "Ưrah rơm, izucun."

t = Turtle(shape="classic", visible=False)
t.speed(0)
t.penup(); t.goto(0, 0); t.pendown()
t.left(180)

passageLst, _ = read(txt)
draw(passageLst)

Screen().mainloop()
```

### Configuration flags in `ItiDrawer.py`

| Flag | Default | Effect |
|------|---------|--------|
| `mazeMode` | `True` | Enable collision avoidance; strokes never cross |
| `exportMode` | `False` | Export to SVG instead of displaying interactively |
| `periodMode` | `True` | Render sentence-final hollow dot markers |
| `centerMode` | `True` | Start drawing from the centre of the canvas |
| `rapidMode` | `False` | Suppress screen updates during drawing (faster) |
| `drawMode` | `False` | Highlight bounding boxes for debugging |

### Exporting to SVG

Set `exportMode = True` in `ItiDrawer.py`. The renderer uses `svg_turtle` in place of the standard turtle module and saves the output to `example2.svg` on completion.

### Scale parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `UNIT` | 50 | Base drawing unit in pixels |
| `SCALE` | 5 | Ratio of ornament features to base unit |
| `MAGNIFICATION` | 20 | Canvas scroll magnification |
| `CHANCES` | 4 | Number of spacing attempts before backtracking in maze mode |

---

## Dependencies

- [`pyqtree`](https://github.com/karimbahgat/Pyqtree) — spatial quad-tree index for collision detection in maze mode
- [`svg_turtle`](https://github.com/donkirkby/svg-turtle) — SVG export backend for turtle graphics
- Python standard library: `turtle`, `math`, `random`, `re`

---

## Related Projects

- [Nguasach](https://github.com/TonyYZ/Nguasach) — cross-linguistic phonetic-semantic corpus; Ítí's phonological structure is designed in part to exhibit the iconicity patterns studied there
- [Aitia](https://github.com/TonyYZ/Aitia) — Bayesian concept learning using a spatial language of thought; the spatial layout logic of the Ítí script shares structural ideas with the image-schema model

---

## Author

Yutong (Tony) Zhou — M1 Cognitive Science, ENS-PSL  
Background in cognitive science, computational linguistics, and embodied semantics.
