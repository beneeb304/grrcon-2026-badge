# Final sweep before firmware access — September 26, 2026

## Outcome

No verified second-stage instruction or badge-specific CTF server has been found. This does not prove the second video is the end of the puzzle. Firmware reading is paused at the user's request. The most useful remaining work is controlled comparison of the badge's observable states using the existing UART, PC0, power, and ground wires.

## Links and video

- Fresh requests to the exact printed links confirm HTTP 301 redirects: https://bit.ly/GrrCON15 points to the original Rick Astley video; https://bit.ly/GrrCON15b points to https://www.youtube.com/shorts/xkK5x4kOaNc. The response bodies are ordinary redirect links, without extra challenge text or URL parameters.
- The second link's public Bitly preview still exposes the same destination. Its creation time is December 24, 2025, as previously recorded. No additional instruction was found in the preview.
- The second video's full YouTube page says "In-N-Out worker calls number 67 and restaurant goes crazy," uploaded by Galaxy Views on October 28, 2025. It is 31 seconds long, has no description, and has no available captions. The scene is a restaurant crowd reacting to an order number. No badge-specific instruction was established from the inspected scene.
- Earlier comment review reached 117 loaded top-level comments and expanded available reply threads, with no explicit GrrCON/Hak4Kidz/CTF instruction or alternate URL found. This remains limited to available comments; hidden or deleted comments cannot be excluded. This sweep did not claim to repeat the entire comment crawl.
- The number 67 has already been rejected at the original person-name prompt. Sending it after successful access and shutdown produced no observed output. These results do not support treating it as the next password.
- The sweatshirt design and video title are possible observations, not established instructions. There is no supported mapping from them to physical chip pins, voltages, EEPROM changes, or a different baud rate.

## Designer and event material

- A fresh public GitHub repository listing returned the same 17 repositories. No public repository for the current anniversary firmware was listed. Public repository absence does not exclude unpublished code or another account.
- The current Hak4Kidz homepage HTML contains a commented-out link to https://ctf.hak4kidz.com/register. The CTF is live and titled "Fractured Timeline: Capture the Flag." Its public page configuration gives June 6, 2026, 14:25–20:30 UTC, matching the Chicago event rather than the September GrrCON event. The public challenges page returned 403; no login, registration, or access bypass was attempted. No current badge linkage was found.
- The h4klab.github.io repository redirects to the main Hak4Kidz website; its custom domain is h4klab.com. The cyphervillagectf.github.io repository's site contains old 2017 event material. Neither yielded a current badge instruction.
- Publicly accessible X/Bluesky material was previously inspected without current challenge instructions. This is not a complete authenticated archive.
- GrrCON's official crypto page has independent ticket challenges, including a current Challenge 19. No reference tying those challenges to this PCB, its links, or Heal's anniversary routine was found. Do not merge the two puzzle tracks based only on the conference name.
- User confirms badge came from admission and included no card, packaging instructions, QR code, or verbal hint.

## Physical and serial clues

- PCB says 0xE (decimal 14); serial banner says 15TH. Reused PCB artwork with newer firmware is one explanation, but not verified. This discrepancy is worth documenting rather than converting directly into a password.
- Acrylic photos are opposite views of one engraving. Jarvis / 50 / 150 may be a handle or credit plus edition numbering; no matching public explanation was found. Jarvis was rejected at the original name prompt. The user does not know whether the engraving was customized.
- The TX arrow led to a working UART; the opposite arrow led to PC0 and a working challenge trigger. Both major marked signals have a confirmed function.
- Five software LED pin numbers map to valid GPIO names. Firmware pin 0 is legitimate software numbering, not a physical package pin 0.
- EEPROM marker is repeatedly 47 52 52 45 01 00: ASCII GRRE followed by two binary bytes. Header, version, and state are hypotheses. Existing dumps have not demonstrated progress after success.
- Saved text captures contain only the two known URLs. They do not contain additional control bytes, but screen hardcopies are not a substitute for a new raw serial capture and cannot exclude characters discarded by the terminal.
- "System shutdown" does not power off the MCU: PC0 remains responsive and can reopen the original challenge. Post-challenge LEDs look normal and SW1 currently appears inactive.
- User confirms SW1 changes LEDs after a clean normal startup at the current 3.3V. This differs from post-challenge operation, where SW1 appears inactive. Similar LED patterns therefore do not prove the same operating state, and supply voltage alone does not explain the observed button difference.
- PC0 triggered from clean normal mode prints the same Rick Astley challenge. Holding SW1 while triggering PC0 also prints the same challenge. Sentinel startup is therefore not required, and the tested combination did not reveal another stage.
- Historical public maker code provides a reason to inspect optical behavior carefully: the 2021 grrcon0xa sketch has an accelerometer-triggered interactive Morse mode, and the older scavenger-hunt repository uses Morse blinking. Those designs have different hardware and are not evidence that this badge's LEDs encode a message. Their button or tap procedures must not be assumed to apply here.
- Existing video measurements show changing groups of neighboring LEDs. Camera motion, exposure, and 0.25-second sampling limit decoding. Neither a repeatable shared message nor true randomness was proved. A stationary high-frame-rate restart capture is the appropriate next optical test if this route is pursued.
- USB remains unresolved: chip VDD is 0V on USB alone and no ground continuity to the chip was found. That does not establish whether USB power reaches the connector itself. A measurement across the connector's own VBUS and GND would distinguish a disconnected/faulty connector path from power that simply does not reach the chip. Do not use CR2032s during USB experiments.

## Remaining experiments, without new soldering

1. Completed: SW1 works on clean normal startup, but appears inactive after challenge completion.
2. Completed: PC0 from clean normal mode opens the same challenge as Sentinel mode.
3. Completed: holding SW1 while triggering PC0 opens the same challenge.
4. If needed, make a stationary 60-second high-frame-rate video starting before power-on. Compare repeated starts of the same mode before trying Morse or five-bit decoding.
5. Clarify the USB measurement reference before making claims about a dummy connector or repairing it.

Avoid unsupported voltage injections, grounding unrelated chip pins, guessing URL suffixes, or changing EEPROM/fuses. There is currently no clue justifying those actions. No firmware access, new soldering, or designer messaging was performed during this sweep.

## Source trail

- https://www.hak4kidz.com/
- https://ctf.hak4kidz.com/
- https://api.github.com/users/Hak4Kidz/repos?per_page=100
- https://github.com/Hak4Kidz/h4klab.github.io
- https://github.com/Hak4Kidz/cyphervillagectf.github.io
- https://github.com/Hak4Kidz/grrcon0xa
- https://github.com/Hak4Kidz/scavenger-hunt
- https://grrcon.com/crypto/
- https://bit.ly/GrrCON15b+
- https://www.youtube.com/watch?v=xkK5x4kOaNc

Fresh fetched page sources and summaries are saved beside this report. Historical terminal and optical measurements remain in the parent captures directory.
