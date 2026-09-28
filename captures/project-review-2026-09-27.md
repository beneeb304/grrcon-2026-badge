# GrrCon 2026 badge: evidence review before firmware access

Reviewed September 27, 2026. This review uses the supplied conversation images, saved terminal histories, four LED recordings and their measurements, prior saved website/comment research, and fresh targeted public searches. Original temporary photo paths have expired; the attached images remain available in the conversation. No badge or Flipper serial device was present during this review, so the remaining hardware tests below have not been performed.

## Assessment

Firmware extraction is not established as a requirement of the intended puzzle. The demonstrated path is coherent: discover UART, enter or bypass Sentinel diagnostics, trigger PC0, follow the first link, enter Rick Astley, and receive the second video link. No demonstrated output gives a next action beyond that second link. A hardware discovery puzzle ending in joke links remains a plausible explanation, not a confirmed ending.

There are still bounded, useful tests using the existing wiring. First, make sure a supposed power cycle actually removes badge power: the powered host TX connection is a possible source of parasitic power through badge RX. This has not been measured on this badge. Two functional questions remain open: the complete cycle of normal SW1 modes, and the purpose of Sentinel Watch Mode. PC0 opening the challenge from normal mode proves that Sentinel is not a prerequisite; it does not explain Sentinel's existence. Most optical effort examined the Sentinel walk animation. Results from that animation cannot exclude a message in a different normal mode.

## Evidence and interpretation

| Item | Established | What it does not establish |
|---|---|---|
| TINY1616 marking, 20-pin package | ATtiny1616 is the identified MCU; working UART is 9600 baud on physical pins 9 TX and 8 RX. | A USB socket does not establish a USB data implementation. |
| TX arrow and opposite arrow | TX led to serial output; physical pin 12 / PC0 pulled low through 10k opens the challenge. | The opposite arrow is no longer an unexplained clue. |
| Sentinel pin list `16, 0, 1, 8, 9` | These are valid megaTinyCore software GPIO numbers, corresponding to PA3, PA4, PA5, PB1, PB0. | They are not physical package numbering; software pin 16 is not physical UPDI pin 16. No pin-zero paradox remains. |
| Sentinel entry versus Watch Mode | SW1 held at startup selects this path. The firmware explicitly ends the five-pin test, then announces Watch Mode. The user reported that subsequent short SW1 presses did not change its behavior even before the Rick Astley challenge. | The initial self-test is partly explained, but the purpose and watched conditions of the continuing Watch Mode remain unknown. A diagnostic mode followed by a shared PC0 watcher is one hypothesis, not a verified implementation. |
| Sentinel LED footage | Five pairs move around the ring; the settled direction sequences differ between recordings. Simple 7/8-bit direction-to-ASCII checks did not yield a readable message. The first five clearly extracted pulses in IMG_5328 traverse the five pairs once, consistent with the printed self-test. | No general proof that the badge has no optical message. Normal modes, other encodings and incomplete startup coverage remain separate questions. |
| `GRRE 01 00` | All 13 complete marker blocks in overlapping saved terminal histories have these same six bytes. The marker is present before a correct answer and on subsequent re-entry. | The 13 blocks are not 13 independent experiments. The binary bytes have no proven version, score, flag or address meaning. They are not an instruction to edit EEPROM. |
| `probe`, `contact`, `handshake accepted` | These appear on the PC0-triggered path. | They do not establish a separate network handshake or programming protocol. |
| `Checking firmware` | The program prints that phrase. | It is not evidence of an actual integrity check, failure, or instruction to extract firmware. |
| Correct answer | `Rick Astley` produces ACCESS GRANTED and the second URL. | Rejected names/numbers do not establish another parser or password prompt. |
| `System shutdown` | It occurs after both success and exhausted guesses. PC0 still responds afterward. | It does not mean electrical power-off or uniquely indicate a successful second stage. |
| SW1 after challenge | It appears inactive although it works after a clean normal startup at 3.3V. | This could be the firmware remaining in another loop; it is not proof of a new puzzle state. |
| `0xE`, `15TH`, `rev. E` | The PCB and serial banner use differing edition/revision labels. | Reused art, revision naming or mistakes are plausible; none is verified. Do not turn them directly into voltages, pin combinations or passwords. |
| Jarvis / 50 / 150 | Those markings are visible on one acrylic engraving viewed from opposite sides. | Handle/credit plus edition numbering is only a hypothesis. Another matching badge or maker explanation would help. |
| R2-D2, skull art, component labels | These are visible PCB details; R2 and D2 also serve as ordinary component references. | No new instruction follows from the artwork alone. |
| RECHARGE micro-USB | No chip power from USB alone and no measured connection between the checked connector points and badge ground were reported. | A completely isolated dummy socket has not been proved. The five contacts have not been fully mapped. |

The software pin mapping was checked against [megaTinyCore's 20-pin variant](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/variants/txy6/pins_arduino.h). That match is strong evidence for ordinary Arduino-style numbering, although the exact firmware source remains unknown.

Further pin-map review provides a concrete engineering explanation for the particular set: software pins 16, 0, 1, 8 and 9 map to the default TCA PWM outputs WO3, WO4, WO5, WO1 and WO0. The sixth default output, WO2, is PB2 / software pin 7 / physical pin 9, already used by the working UART TX. Thus the listed set is exactly the other five default TCA PWM outputs. PWM is useful for LED brightness control. This is strong support for deliberate hardware selection, although it does not prove the designer's intent or that TCA is actually configured in the unread firmware. The array order may follow LED layout; that is a separate inference. No numerical probability or secondary cipher is established. Sentinel Watch Mode remains unresolved independently of the pin-list explanation.

## Website and social clues

The printed URLs remain the most strongly grounded online clues. Prior direct requests established the first as the Rick Astley video and the second as the Galaxy Views order-67 Short. The second video's available description, captions, Bitly preview and previously reviewed visible comments provided no badge-specific next instruction. The earlier comment review covered the available loaded comments; it cannot exclude platform-hidden or deleted material. No fresh complete comment crawl was performed in this review.

Fresh targeted searches for GrrCon 2026 with the maker, MCU and distinctive terminal phrases found no current badge walkthrough or next-stage instruction. The [official event page](https://grrcon.com/) confirms September 24–25, 2026. The [Hak4Kidz homepage](https://www.hak4kidz.com/) separately lists the June Chicago CTF activity and September GrrCon village; neither establishes that the June CTF is the badge destination. GNU Radio's similarly named GRCon CTF is a different event.

The saved maker repository listing includes historical badge projects, but no identified current firmware. Historical Morse features demonstrate the maker has used optical puzzles before, not that this particular mode encodes Morse. The [maker's public custom-backing advertisement](https://www.linkedin.com/in/davidschwartzberg) supports decorative customization as an alternative explanation for rim text; it does not identify this acrylic plate.

The terminal explicitly names @Hak4Kidz for updates. Maker clarification or a matching attendee badge remains a useful source unavailable from the current hardware captures. A focused question would be whether the second video is the intended ending of the 2026 admission-badge challenge, rather than a request for all solutions. No message was sent.

## Remaining tests, in order

### 0. Verify an actual cold start

The present bidirectional wiring includes Flipper TX pin 13 through 1k to badge RX physical pin 8. When the badge's VDD supply is removed while the Flipper remains powered, that high signal can potentially feed the badge through input protection circuitry. A series resistor limits current but does not guarantee electrical isolation. Microchip documents [power through I/O](https://onlinedocs.microchip.com/oxy/GUID-D6FD9F43-8DC4-476E-A55E-AA21FA1CC865-en-US-4/GUID-E76F3635-A8C2-4E47-B408-07867944877A.html) and [AVR input clamp diodes](https://onlinedocs.microchip.com/oxy/GUID-6AC9F79C-CD9D-4DEE-B7A9-57FB68C0D274-en-US-3/GUID-C94F9D0C-A2A7-461E-B1D6-48B2AD6585B2.html). Applying that mechanism to this wiring is a hypothesis, not an observed diagnosis.

Before a cold-start test, unplug the Flipper-TX-to-badge-RX jumper at the breadboard/Flipper end, then remove badge VDD power. Leave batteries and badge USB disconnected. Confirm approximately 0V between badge VDD physical pin 1 and GND physical pin 20. Keep the badge-TX-to-Flipper-RX listening connection only if VDD remains approximately zero; any remaining powered signal path must also be disconnected if it holds VDD up. Set the desired switch/PC0 state, then restore the 3.3V supply. Reconnect the host transmit jumper only after the badge is powered and an answer is needed. No soldering is required.

### 1. Catalogue normal modes

Use the proven 3.3V setup, batteries removed and badge USB disconnected. Start normally with SW1 released and PC0 disconnected. Keep UART at 9600 and begin recording before startup. Observe the initial LED behavior, then make one short SW1 press and release every 10 seconds. Record each distinct mode until the sequence visibly wraps; stop after 12 presses if a wrap is unclear. This is a finite exploratory limit, not a claimed firmware mode count.

Note whether any mode has a repeating word-like pattern, long pauses, LED counts, or new UART text. Specifically note whether normal cycling reaches the same five-pair walk seen in Sentinel, and whether SW1 remains responsive there. A visual match would not prove identical internal state. Only a distinctive candidate needs another detailed video. Once the short-press cycle is documented, one approximately three-second hold-and-release during normal operation is a reasonable separate control test. Repeat that single hold-and-release in a fresh Sentinel session with PC0 disconnected and before entering the challenge, to check whether the boot-selector button can also exit or change Watch Mode. Neither is a known secret gesture.

The three observed cases are: normal startup responds to short SW1 presses; Sentinel Watch Mode reportedly does not; post-challenge operation reportedly does not. The latter two could share a waiting loop, but the behavioral similarity alone cannot establish that. The earlier failure of `67` after shutdown does not test every possible UART interaction in fresh Sentinel Watch Mode.

Update from the user's long-hold test: in Sentinel, short clicks do nothing, but a long hold turns off all rim LEDs while leaving the middle LED lit. The user reports the same long-hold behavior in normal mode, where short clicks cycle all-on, pulsing, random and other sequences. Therefore Sentinel does respond to SW1; the earlier broad description of button inactivity applies only to short clicks. The matched long-hold behavior suggests a common display-control behavior, while the short-click mode selector differs. It does not prove shared source code or complete MCU shutdown, and it weakens the idea of a Watch loop that ignores SW1 entirely. Wake/recovery behavior after the long hold has not yet been recorded. Next compare one short click and, if needed, another long hold from this rim-off state, without triggering PC0, then check whether any recovered animation remains in Sentinel or permits normal short-click cycling.

### 2. Complete the recorded startup combinations

| SW1 at power-on | PC0 at power-on | Status |
|---|---|---|
| Released | Disconnected | Normal mode confirmed. |
| Held | Disconnected | Sentinel diagnostics confirmed. |
| Released | Connected to GND through existing 10k | No clearly labelled result in the saved investigation. |
| Held | Connected to GND through existing 10k | No clearly labelled result in the saved investigation. |

For each missing case, use the verified cold-start procedure above and establish the input state before applying badge power; release SW1 and disconnect the PC0 pull-down after about two seconds, then observe. This differs from the already completed test of holding SW1 while pulsing PC0 after a normal boot. If both reproduce the same prompt, record that and stop pursuing these combinations. No other chip pins need to be grounded.

### 3. Preserve a complete raw UART session alongside those tests

Our meaningful challenge evidence is saved as terminal hardcopies/screenshots. Existing binary captures are empty or only 13/16 bytes from the earlier faulty-contact stage; they are not complete clean sessions. Capture original bytes at 9600, 8N1, with no flow control, from startup through a PC0 trigger, the exact working name, and at least 30 seconds after shutdown. Keep the raw binary and a timestamped readable/hex rendering. Use a single serial connection owner so the terminal and logger do not consume each other's data. Pace transmitted characters as in the successful earlier test.

Inspect for backspaces, carriage-return overwrites, escape sequences, non-printable payloads, an incomplete final line, and delayed output. This closes a genuine evidence gap; there is currently no affirmative evidence that such hidden bytes exist. It is ordinary serial logging and requires no firmware extraction.

### 4. Resolve the USB socket electrically

Remove all badge power: batteries, badge USB, and external Flipper connections. Use continuity/resistance measurements to map all five small USB contacts against the already soldered badge GND, VDD, TX, RX and PC0 leads. Check the shell separately. Give contacts temporary left-to-right labels tied to a photograph, rather than guessing standard USB pin numbers from viewing orientation. Record resistance, since a resistor-mediated connection may not beep.

A direct connection to known signals could reveal an intended alternate access connector. No connection to those five nets would lower its priority, but would not prove isolation from every other MCU pin; that would require a fuller unpowered map or schematic. The photos alone cannot certify the internal connections. There is no reason yet to inject voltage into the socket or bridge its contacts, and RECHARGE does not make CR2032 cells rechargeable.

## Stop rule

If normal modes, the two recorded startup gaps and raw UART add nothing, and USB mapping reveals no useful connection, there is no established next action in the available clues. At that point the honest alternatives are maker/attendee confirmation, accepting a possible joke ending, or inspecting an unlocked firmware image to answer what else is implemented.

The prepared Flipper reader has been built and tested in software but has not been validated on this hardware. A later read would begin with device identification and lock status and would not erase or change fuses. No firmware read was performed as part of this review.

## Local evidence

- `captures/access-granted.txt`: early failed and successful sessions, including both shutdown paths.
- `captures/pc0-repeat-confirmed.txt`: successful re-entry and unchanged marker; later rejected guesses.
- `captures/final-sweep/review.md`: prior web and physical sweep, with some follow-up experiments now completed.
- `captures/video/new-recordings-review.md`: scope, measurements and limits of the latest optical analysis.
