# MindWords — sample dictionary entries

Three of the eleven entries, as documented in the project report (sections 5.2–5.4). Examples are taken from the Sketch Engine concordance of the *self improvement* corpus (GDEX-sorted); collocations come from Word Sketch, Visual Word Sketch and the CQP query `[pos="N.*"][word="anxiety"]`.

Definitions below are short paraphrases. In the dictionary itself they were checked against the reference dictionaries listed in the report (Cambridge Dictionary for English, DWDS/Duden for German, Almaany, Le Robert, RAE).

---

## anxiety
*noun* · domain: **Emotional States** · ~396 per million tokens in the full deduplicated comment set

**Definition.** A feeling of nervousness or worry about something happening now or that might happen later. In the comments it is mostly talked about as a clinical, nameable condition people *have*, *experience* or try to *reduce*.

**Corpus examples**
- *my social anxiety has been so bad lately*
- *having this constant unbearable anxiety every day*
- *Anxiety is not an enemy – it is a signal*
- *anxiety and depression are so interconnected*
- *understanding my social anxiety through this video*

**Common group words**
`social anxiety` · `anxiety disorder` · `lessen anxiety` · `reduce anxiety` · `anxiety attack` · `my anxiety` · `experience anxiety` · `separation anxiety`

**Usage note.** Often the head of a noun compound (*separation / job / death / shame anxiety*), including the creative coinage *trickle-down anxiety*. A visible counter-narrative reframes anxiety as a signal rather than an enemy (*Anxiety is not an enemy*).

**Contrast with *healing*.** Word Sketch Difference shows *anxiety* as concrete and clinically framed (modifiers *social, debilitating, constant, serious*), while *healing* is abstract and spiritual (sole modifier *spiritual*; compounds *healing art, healing frequency*).

> *You don't have to control your thoughts. You just have to stop letting them control you.*

---

## discipline
*noun* · domain: **Self-Improvement** · ~76 per million tokens

**Definition.** The ability to control your own behaviour and keep doing what you planned, built up through regular practice. In general English the word leans toward rules, training and punishment imposed by others; in this corpus it is almost always **self**-discipline.

**Corpus examples**
- *discipline beats motivation every single time*
- *small daily discipline leads to big progress*
- *discipline is the gateway to freedom*
- *you need to build discipline like a muscle*
- *conscious discipline is the start of any real change*

**Common group words**
`build discipline` · `daily discipline` · `little discipline` · `discipline and mindset` · `self-discipline` · `practice discipline` · `discipline is a gateway` · `discipline over motivation`

**Usage note.** Strongly metaphorical: *discipline is a gateway / an engine / freedom*, and *discipline muscle* (something you train). In the reference corpus (English Web 2021) the profile is institutional instead — *academic, scientific, fiscal, strict* discipline that people *impose, enforce* or *instill*.

> *Discipline is the bridge between goals and accomplishment.* (commonly attributed to Jim Rohn)

---

## mindset
*noun* · domain: **Self-Improvement** · ~126 per million tokens

**Definition.** A person's habitual way of thinking and the attitudes that come with it.

**Corpus examples**
- *a discipline mindset is everything*
- *change your mindset and change your life*
- *mindset is the start of all progress*
- *responsible mindset training takes time*
- *your mindset determines your outcomes*

**Usage note.** In the comments *mindset* collocates mainly with *discipline, training, progress* — a personal, self-directed register. In the reference corpus it is something organisations *change, adopt, shift, cultivate*, with modifiers like *entrepreneurial, growth, abundance, scarcity*. Closest thesaurus neighbours: *attitude, mentality, thinking, paradigm, worldview, ethos*.

**German:** *Mentalität, Denkweise* — the characteristic way of thinking, viewing and behaving of a person or group.

> *Whether you think you can, or you think you can't — you're right.* (commonly attributed to Henry Ford)

---

## All entries

| Domain | Entries |
|---|---|
| Emotional States | anxiety, overthinking |
| Self-Improvement | discipline, mindset, self-education |
| Support and Encouragement | empathy, you are not alone |
| Struggle and Recovery | healing, self-worth |
| Advice and Reflection | mindfulness, self-motivation |

Per-million figures are computed by [`scripts/corpus_stats.py`](../scripts/corpus_stats.py) over all 14 source files (deduplicated), counting all inflected forms; they differ from the Sketch Engine figures in the report, which refer to the two-video subcorpus.
