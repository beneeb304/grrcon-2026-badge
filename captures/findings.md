# GrrCon badge investigation

## Complete welcome-package pages, 2026-09-29
- Preserved the attendee photos as [word search](papers/glimpsing-the-shoggoth.jpg) and [welcome directive](papers/welcome-directive.jpg). They are distinct handouts; neither photo contains a visible badge wiring diagram, UART command, password, QR code, or CTF URL.
- The welcome directive says, "A word about anomalies: artifacts have been concealed throughout the facility for the engaged human to discover. Keep your sensors open." This is the strongest new lead, but it names the facility rather than the electronic badge. The rest of the page mostly describes conference tracks, sponsors, social activities, and an AI-versus-human theme. "Your badge is scanned" and the hardware-security-key comparison read as thematic prose; no scanning hardware or badge-specific procedure is identified.
- The separate sheet is titled "Glimpsing the Shoggoth" and asks attendees to find 100 terms in a word-search grid. Visible terms include PROMPT SLOP FACTORY, AI GLAZING, AI POLLUTION, SHARE BAIT, CHATBOT PSYCHOSIS, HALLUCINATION, ENGAGEMENT BAIT, STOCHASTIC PARROT, MODEL COLLAPSE, and UNCANNY VALLEY. The sheet provides no word bank or explicit rule for deriving a second message. Its full 100-term solve and leftover letters have **not** been verified, so it remains a separate possible paper puzzle rather than a demonstrated badge stage.
- [Bryan Smith's published badge write-up](https://www.redlinecybersecurity.com/blog/hacking-the-grrcon-2026-badge) independently reports the same PC0 trigger, Rick Astley answer, and two joke redirects, and says he completed the badge challenge. It does not mention either handout. Its claim that EEPROM byte 0x04 is a solved-stage flag and 0xEA is a counter conflicts with our two matching dumps and direct code analysis (0xEA is FF here; 0x04 is part of a fixed startup marker). Treat its outcome as corroboration, not a substitute for our measurements.

## Printed welcome text, 2026-09-27
- Attendee paper excerpts describe a scanned badge, a "mostly harmless" threat profile, "Overlords," and a first badge "like a hardware security key." The [official 2026 schedule](https://grrcon.com/schedule/) has an **OverLords** track, and the [presentations](https://grrcon.com/presentations/) emphasize human-versus-AI themes. These words are consistent with event narrative rather than a demonstrated badge instruction.
- Case-insensitive scan of readable flash strings found none of `overlord`, `harmless`, `threat`, `profile`, `initialized`, `security key`, `curiosity`, `skeptic`, or `scan`. Static string absence does not exclude an encoded clue, but the known USB port does not enumerate or power the MCU and firmware offers only the identified UART challenge.
- Next check: inspect the complete paper page, especially headings, footnotes, layout, QR codes, and any explicit badge/CTF directions. Keep the conference's separate contests distinct from this admission badge. No basis yet to try these welcome phrases as serial passwords.

## Acrylic markings and final video, recheck
- The photographed clear acrylic layer reads `Jarvis`, `50`, and `150`. A [public repost of a Hak4Kidz announcement](https://www.linkedin.com/in/davidschwartzberg) describes a separately offered **custom GrrCON 0xE backing** that can carry a handle or other personal text and sits behind the core badge. This makes a custom/decorative origin for `Jarvis` plausible, but we have not verified that this exact acrylic piece is one of those preorders. `50 / 150` plausibly denotes an edition number, but no maker label or second example confirms that interpretation.
- Neither `Jarvis` nor ASCII `50`, `150`, or `67` appears as a printable token in the flash image. The EEPROM contains only the six-byte startup marker and erased bytes; the separate 32-byte User Row is entirely erased. These markings are not demonstrated firmware inputs or saved state.
- The linked 31-second YouTube video predates the badge. Its number `67` is the one conspicuous possible clue, but no badge-specific instruction, URL, or code was found in sampled frames or inspected comments. Audio and every individual frame have not been exhaustively reviewed. The second Bitly URL may be the intended final joke, though that is an inference, not a confirmed author statement.

## Confirmed
- Chip marking: Atmel TINY1616, 20-pin SOIC.
- TX soldered to physical pin 9 / PB2; GND to physical pin 20.
- Two CR2032 cells, about 2.9 V each; chip supply/raw TX about 5.5 V.
- Equal 10 kOhm divider gives about 2.7 V; midpoint to Flipper pin 14 RX, GND to pin 11.
- Flipper UART loopback passed, including disconnecting jumper to exclude local echo.
- No received bytes on initial button-only sweep of 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400 baud.
- Holding SW1 during battery insertion enters Sentinel mode and emits readable UART at 9600 baud.
- Output tests firmware pins 16, 0, 1, 8, 9, then says Sentinel Mode Complete / Entering Sentinel Watch Mode.
- USB-only gives 0 V at chip, with known-working cable; no badge device enumerates. No continuity found from shell or outer contacts to chip power/ground. Connector function remains unconfirmed.

## Video observations (IMG_5316, IMG_5318)
- Clips are about 46.3 and 53.0 seconds (updated from decoded asset metadata).
- Center LED stays lit in inspected portions after startup.
- Rim LEDs commonly illuminate as five neighboring two-LED groups, sometimes several groups at once.
- No clear short repeating sequence shared by the clips was established. Do not infer true randomness or encoded text from this.
- Brightness varies; camera sampling and hand movement limit exact optical bit extraction.
- Live serial log has additional startup messages and non-text bytes around restarts, but no new readable Watch Mode event description.

## Next route
Read firmware through UPDI if accessible and unlocked. Physical pin 16 / PA0 is UPDI, fifth leg down on right with dot at upper-left. Arduino Uno (ATmega328P) can run jtag2updi, with D6 as UPDI through a resistor. Verify board model, voltage/power wiring, software and autoreset before connecting. Read device ID / lock state first. Never erase or change fuses to unlock: preserve original firmware.

## Challenge access confirmed
- Normal startup LED sequence differs from Sentinel mode (user observation).
- PC0 physical pin 12 rests high; pulling toward GND through 10 kOhm triggers handshake / challenge banner.
- Badge now powered from Flipper 3V3 pin 9 into chip VDD pin 1, CR2032 cells removed, badge USB unplugged.
- UART TX physical pin 9 direct to Flipper RX pin 14; badge RX pin 8 via 1 kOhm to Flipper TX pin 13.
- Accepted code: Rick Astley. Richard Paul Astley was rejected.
- Successful banner gives https://bit.ly/GrrCON15b then System shutdown.
- Link resolves to YouTube Short xkK5x4kOaNc, metadata title: In-N-Out worker calls number 67 and restaurant goes crazy (Galaxy Views). No actual CTF site established.

## Link and comments follow-up
- Bitly direct response contains only a redirect; public plus preview saved as captures/bitly-preview.html.
- Preview title is "- YouTube", created Dec 24 2025 05:48 UTC, destination https://www.youtube.com/shorts/xkK5x4kOaNc. No additional puzzle text found.
- Inspected YouTube Top comments, then Newest through the end of 117 loaded top-level entries; expanded reply threads and Show more replies, plus longer text. No badge reference, CTF URL, or explicit puzzle instruction found in loaded comments/replies. This cannot exclude deleted or platform-hidden comments.
- 67 remains an unconfirmed clue from the Short itself. Do not assume it is a password, EEPROM address, or instruction to connect physical pins 6/7.

## Second investigation and next experiments
- Inspected designer's public GitHub repository list: existing badge projects include grrcon0xa (2021 ATmega328P skull badge), badge2018, fordbadge, H4K-badge-2019, H4K-cryptex. No current 0xE/15th badge source or challenge instructions found there.
- Publicly accessible X posts and Bluesky author feed did not reveal current badge instructions. X does not expose the entire profile without login, so this is not an exhaustive social archive.
- LinkedIn custom backing post refers to a cosmetic add-on; linked product currently returns 404. Not evidence of a challenge solution.
- Current serial history confirms 67 rejected twice at the person-name prompt. Chip still prints GRRE / 01 00 in available startup marker dumps.
- PC0 normally disconnected from GND (user confirmed). User confirms a momentary PC0-to-GND trigger after shutdown reprints the original Rick Astley challenge without a power cycle. This proves the badge remains responsive after the shutdown message; no new challenge stage has been established.
- Terminal subsequently showed original name prompt; submitted Rick Astley. Burst transmission corrupted input and used one attempt; 250ms per character plus LF produced ACCESS GRANTED. LF is confirmed accepted; CR alone did not submit in this test.
- Sent paced 67 + LF after ACCESS GRANTED and shutdown. No echo or new output appeared during the observation. Saved captures/retrigger-unlock.txt and post-unlock-67.txt. This does not prove every other input is disabled.
- Acrylic layer photos IMG_5325 / IMG_5324 show the same etching from opposite sides (mirrored on the back), with Jarvis, 50, and 150 on the rim. The arrangement could mean edition 50 of 150 plus a handle or credit, but this is unverified. User does not know whether personalized or whether other badges have different numbers. Public exact-marking searches found no matching explanation. Custom GrrCON 0xE backing advertisements exist, but do not identify this specific layer.
- Latest saved terminal history captures/pc0-repeat-confirmed.txt shows 67 and Jarvis rejected at the original person-name prompt, with one attempt left. Do not spend the remaining attempt on speculative engraving codes.
- User confirms that after successful challenge/shutdown, LEDs appear to return to normal startup operation and pressing SW1 has no effect. No second stage established through this button experiment. Treat the shutdown as the end of the observed challenge routine, not evidence that the MCU loses power.
- Final sweep comparison: user confirms clean normal startup at 3.3V has working SW1 LED changes. Post-challenge SW1 inactivity therefore differs from normal operation even if LEDs look similar. PC0 from clean normal mode produces the same Rick Astley challenge. Holding SW1 while triggering PC0 after a normal boot also produces that challenge.
- EEPROM marker repeated across saved captures: 47 52 52 45 01 00, ASCII GRRE followed by two binary bytes. Header/version/state interpretations remain hypotheses; unchanged dumps do not establish progress. Dots are the terminal's non-printable-byte placeholders.

## Flipper reader preparation
- User cannot find Uno USB-B cable, prefers minimal soldering, uses official stable Flipper firmware, and has not soldered UPDI yet.
- Downloaded dhahaj/UPDI-Programmer source under tools/flipper-updi. Stock official USB-UART bridge source applies baud but not requested parity/stop bits; UPDI requires 8E2, so it is not a straightforward substitute for a dedicated UPDI app.
- Prepared local UPDI Reader variant: removed flash/erase menu entries, dispatcher rejects both operations, do_connect refuses allow_erase, locked-device message preserves firmware. Adapted Momentum-only settings header call for official SDK.
- Built successfully against official release 1.4.3, target 7, API 87.1. Artifact tools/flipper-updi/dist/updi_prog.fap. Portable protocol tests: 120 checks, 0 failures. No hardware validation, app installation, or badge firmware read yet.
- Intended wiring: Flipper 9 3V3 to badge physical 1 VDD, Flipper 11 GND to badge physical 20 GND; Flipper 13 TX via 1k to common UPDI node, Flipper 14 RX direct to that node, node to badge physical 16 PA0/UPDI. One new badge solder joint; existing power/GND reused. Batteries removed, badge USB and old TX/RX/PC0 wires disconnected from external circuits. All badge power must be 3.3V for this wiring.
- Flipper fallback: https://github.com/dhahaj/UPDI-Programmer explicitly lists ATtiny1616, read signature/fuses and Dump Flash, Momentum SDK mntm-012. Author reports emulator validation only and says hardware testing still required. Do not treat this as a verified turnkey reader. Existing AVR ISP app uses the wrong programming interface for this chip. No firmware read, installation, erase, or fuse changes attempted.

## September 27 evidence review before firmware access
- Firmware reading remains paused. See captures/project-review-2026-09-27.md for the current assessment and finite remaining tests.
- The visible challenge path may end in the second joke link; no further instruction has been established.
- Shutdown appears after both correct-answer success and exhausted guesses. It is not by itself evidence of a new stage.
- All 13 complete EEPROM marker blocks in overlapping saved histories match GRRE / 01 00. These are not 13 independent tests and do not establish the bytes' meaning.
- Latest optical review covered the settled Sentinel-style walk, not a catalogue of normal SW1 modes. Normal-mode cycling is the highest-priority unrecorded test.
- Other remaining gaps: explicit PC0-low-at-power-on tests with SW1 released/held, complete raw UART logging, and unpowered mapping of all five USB contacts.
- Before interpreting more startup tests, exclude parasitic power from the powered Flipper TX pin 13 through 1k to badge RX physical pin 8. This is a wiring-based hypothesis, not a measured fault. Disconnect that host-transmit jumper before removing badge VDD and verify VDD-to-GND approximately zero; reconnect transmit only after badge power is restored. See the review's cold-start procedure.
- No Flipper serial device was present during this review; no new live badge tests were performed.
- User correctly highlights that Sentinel's purpose remains unexplained despite PC0 also working in normal mode. Separate the initial five-pin self-test from the explicitly announced continuing Sentinel Watch Mode. Earlier user observations report short SW1 presses inactive in Watch Mode before the challenge, as well as after challenge completion. Shared waiting-loop behavior is a hypothesis. Next normal-mode catalogue should compare its patterns with Sentinel, followed by a bounded long-press test in fresh Sentinel before any PC0 trigger.
- Pin-list review: 16,0,1,8,9 correspond to default TCA PWM outputs WO3,WO4,WO5,WO1,WO0. The missing sixth default output WO2 is PB2 / software 7 / physical 9, used by UART TX. This provides a strong ordinary hardware explanation for the exact LED pin set; actual timer configuration and design intent remain unverified. Source: megaTinyCore txy6/pins_arduino.h peripheral table.
- New direct button observation: Sentinel ignores short clicks but responds to a long hold by turning off every rim LED while leaving the middle LED lit. Normal mode has the same long-hold behavior; its short clicks cycle all-on, pulsing, random and other sequences. SW1 is therefore not entirely ignored in Sentinel. Common long-hold display control is suggested, but shared code and MCU power-down are unproved. Wake/recovery behavior is the next bounded test, keeping PC0 disconnected.

## 2026-09-27 read-only UPDI backup
- Atmega328P Uno was programmed with the upstream ElTangas jtag2updi prebuilt 16 MHz image. Badge batteries, badge USB, and Flipper were disconnected; Uno USB supplied badge VDD through existing pin-1 lead at measured 5 V. Uno GND -> badge physical pin 20; Uno D6 -> 4.7k series resistor -> badge pin 16 PA0/UPDI. No capacitor was needed for this Uno on this Mac; avrdude sign-on required one automatic retry but succeeded.
- Native Apple Silicon avrdude 8.3, `-c jtag2updi -p t1616 -b 115200 -n`, identified signature `1E 94 21`, silicon revision 0.1. Flash and EEPROM were each read twice with `-U ...:r:...:i`; pairwise SHA-256 hashes match exactly. No chip erase or write request was issued. Dumps are in captures/firmware. The flash HEX holds bytes through 0x2953; Intel HEX output omits trailing erased FF region of the 16 KiB address space.
- Firmware printable strings include all observed UART text: EEPROM marker dump, intro, Rick Astley prompt, `ACCESS GRANTED`, final bit.ly/GrrCON15b, `System shutdown`, and Sentinel test/watch messages. Also `Too many incorrect guesses.` No additional plain-text URLs or prompts were found. This does not rule out encoded data or non-obvious program logic.
- EEPROM dump is 256 bytes: `47 52 52 45 01 00` at offsets 0..5; all remaining bytes FF. This corroborates the earlier marker dump. Firmware control-flow analysis shows these six bytes are an initialization marker, not a saved challenge stage.
- Preliminary AVR disassembly locates a startup conditional in the main routine around flash address 0x1594 that selects the Sentinel branch. That branch prints `Entering Sentinel Mode...`, iterates the LED pin-test messages, prints `Sentinel Mode Complete` and `Entering Sentinel Watch Mode...`, then enters an LED/watch loop around 0x164a. A branch from the watch loop goes to the normal operating-mode section at 0x1974. The exact trigger for that branch and any less-obvious side effects remain to be resolved; there is no separate plain-text challenge string associated with Sentinel.

## Offline Sentinel and LED-path review
- The firmware's `random()` routine matches avr-libc's Park–Miller implementation, including its default seed and multiplier. Sentinel Watch repeatedly uses it to choose among the five LED pins and vary the display. This supports a generated animation rather than a fixed prerecorded optical code, while not mathematically excluding a deliberately encoded algorithm.
- SW1 short presses increment a five-state counter in shared input code. Normal operation branches on that counter for five LED routines; Sentinel Watch never reads it. This explains the otherwise puzzling short-press difference. A hold of roughly two seconds enters a shared display/sleep path, agreeing with the common long-hold effect. Its exact wake/transition behavior remains unverified.
- Both modes poll PC0 through the same challenge handler. The repeated Rick Astley prompt from either mode is expected from this code; it does not indicate a separate Sentinel stage. Detailed addresses and limits are recorded in captures/firmware/analysis.md.
