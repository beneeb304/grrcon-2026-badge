# GrrCon 2026 anniversary badge investigation

Notes and read-only captures from investigating a GrrCon 0xE anniversary admission badge. The badge uses an ATtiny1616. This is an investigation record, not badge firmware source code.

## Where to start

- [Current findings](captures/findings.md) and [project review](captures/project-review-2026-09-27.md)
- [ATtiny1616 badge pinout](output/pdf/attiny1616-badge-pinout.pdf)
- [Terminal captures](captures/) and [LED/video analysis](captures/video/new-recordings-review.md)
- [Verified firmware and EEPROM backup](captures/firmware/)
- [Firmware control-flow and Sentinel LED analysis](captures/firmware/analysis.md)
- [Full nonvolatile-memory and alternate-answer audit](captures/firmware/deep-audit.md)
- [GrrCON15b YouTube Short review](captures/video/youtube-short-review.md)

The badge's UART challenge is triggered by PC0. The answer `Rick Astley` reveals the `GrrCON15b` link. Sentinel mode is selected at startup by holding SW1; its watch display uses a pseudorandom LED routine. The normal animation modes are selected by short SW1 presses, but Sentinel does not display those modes.

## Read-only firmware capture

Two flash reads matched byte-for-byte, as did two EEPROM reads. Two subsequent User Row reads and two fuse reads also matched. The signature was `1E 94 21` (ATtiny1616). The EEPROM begins `47 52 52 45 01 00` (`GRRE` plus two binary bytes); remaining locations read as `FF`. The 32-byte User Row is all `FF`. The flash backup contains all serial text observed so far, including Sentinel messages. No extra plain-text challenge URL was found.

The upstream [jtag2updi](https://github.com/ElTangas/jtag2updi) image was uploaded to an ATmega328P Uno. With badge batteries and USB disconnected, Uno 5V powered badge pin 1, Uno GND connected to badge pin 20, and Uno D6 connected through 4.7kΩ to badge pin 16 (UPDI). The chip ran at 5V. Native avrdude 8.3 used `-c jtag2updi -p t1616 -n` and read-only `-U ...:r:...` operations. There was no erase or write request to the badge. The Uno image and upstream license are retained under `tools/jtag2updi/` for reproducibility.

The local experimental Flipper UPDI reader was built and simulated but never tested on the badge. Its separate upstream checkout and downloaded SDK are intentionally excluded from this repo.

## Scope of the files

Generated video frames, web page caches, downloaded toolchains, and the separate Flipper checkout are excluded to keep this repository small. Original phone photos and videos were shared in the chat but are not present in this workspace. This repository is private because it includes a complete firmware dump.
