# New LED recordings — September 27, 2026

IMG_5327.mov: 57.90 seconds, 1,736 decoded frames, approximately 29.98 fps.
IMG_5328.mov: 63.99 seconds, 1,919 decoded frames, approximately 29.99 fps.
All frames were decoded sequentially. The comparison uses the portion after 10 seconds, to reduce hand motion and startup ambiguity. The recordings are steadier than the earlier pair but are still hand-held; they are not independently verified complete captures of identical startup procedures.

## Observed structure

Ten rim LEDs operate as five adjacent pairs. Above the selected brightness threshold, paired LEDs agree on their state for approximately 98–99.9% of analyzed frames. The central indicator is excluded.

There are 119 measured lit bursts in the settled portion of IMG_5327 and 132 in IMG_5328. Median burst duration is about 0.30 seconds. In IMG_5328 all 131 successive dominant-pair changes are exactly one pair around the ring: 66 clockwise, 65 counterclockwise. IMG_5327 has 59 clockwise moves, 57 counterclockwise moves and two repeated dominant groups, with some measurement uncertainty. Changing detection thresholds from 60 to 140 preserves the exact move counts in IMG_5328.

Most frames light one pair or two neighboring pairs. IMG_5328 has no analyzed frames with separated active pairs or more than two active pairs. This restricted state pattern is consistent with a walk around the LED ring, rather than independent five-bit symbols.

## Repeatability and decoding

Across time offsets within ±20 seconds and requiring at least 25 seconds of overlap, the highest exact active-mask agreement is approximately 17%. Shared dim frames are excluded from this calculation. The extracted direction streams do not match over a sustained sequence. They share at most 12 consecutive direction bits in the analyzed portion.

A clockwise/counterclockwise binary interpretation was tested as 7- and 8-bit ASCII, with all byte offsets, inverted polarity, and both bit orders. No coherent readable message was established. There is no clear aggregate short/long Morse timing split or letter/word pause structure. These checks do not exclude encryption, another encoding, per-channel timing, or a message confined to an unexamined startup event.

The practical conclusion is a structured, changing walk animation with no verified message. More casual video recording is unlikely to settle the puzzle. A read-only firmware inspection remains an evidence-gathering option, not a proven requirement of the intended challenge.

## Saved evidence

Per-frame LED brightness: 5327-led-counts.csv and 5328-led-counts.csv.
Extracted bursts: 5327-events.json and 5328-events.json.
Comparison: new-comparison.json.
Binary hypotheses: direction-decode-check.json.
Frame validation: 5327-reader-check.png and 5328-reader-check.png.
