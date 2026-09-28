# Full flash and nonvolatile-memory audit, 2026-09-27

Read-only analysis of the matching ATtiny1616 flash, EEPROM, User Row, and fuse captures. Byte addresses refer to `attiny1616-flash-1.bin`. This is an evidence-based audit of the captured image, not a guarantee against every conceivable obfuscation or hardware behavior.

## Capture integrity and layout

- The two Intel HEX flash files have identical SHA-256 hashes; so do the two EEPROM files. The HEX checksums validate. Reconstructing the 16 KiB address space from the flash HEX leaves `0x16ac` (5,804) erased `FF` bytes after the last programmed byte at `0x2953`.
- Executable code and library routines occupy approximately `0x0000`–`0x23bf`. Small tables and pin data occupy `0x23c0`–`0x242c`. Readable messages and artwork occupy `0x242d`–`0x2941`. The final 18 bytes at `0x2942`–`0x2953` are the C runtime's initialized RAM data, copied to SRAM `0x3800`–`0x3811` by startup code at `0x00a4`–`0x00b8`.
- The 109-byte table region has low byte entropy (3.42 bits/byte), with indices, masks and pin values. It does not resemble a compressed or encrypted payload. This is only a heuristic; low entropy cannot rule out an encoding.
- Across the complete flash image, the exact lowercase string `rick astley` occurs once, `http` occurs twice, and ASCII `67` does not occur. The two `http` links are `https://bit.ly/GrrCON15` and `https://bit.ly/GrrCON15b`; the introductory text also names `www.hak4kidz.com`.
- The complete 256-byte EEPROM dump contains `47 52 52 45 01 00` (`GRRE` plus `01 00`) at offsets 0–5 and `FF` everywhere else.
- The ATtiny1616 also has a separate 32-byte [User Row](https://onlinedocs.microchip.com/oxy/GUID-9175774B-9B45-45D7-A62D-28F07E411073-en-US-4/GUID-3D0F3081-1873-420A-B2FF-4BEF4DCE4083.html) at data address `0x1300`. Two subsequent read-only UPDI captures match and contain 32 `FF` bytes. It holds no programmed clue on this badge, and no direct User Row read or write was found in the application disassembly.
- Two read-only fuse captures also match: `00 00 02 FF 00 F6 04 00 00 FF` at fuse offsets 0–9. Per the [ATtiny1616 fuse summary](https://onlinedocs.microchip.com/oxy/GUID-4B32B28F-63FC-4320-842D-ECC5E5164A23-en-US-3/GUID-BFA327BB-5EC7-45B1-BC8D-47D891525636.html), `APPEND=00` and `BOOTEND=00`, so the fuses do not mark a separate application-data or boot partition. These are configuration bytes, not an additional text store. The factory signature row was not dumped; it holds device identity and calibration data, and no application read of it was identified.

## Secret-name check

The only UART input-reading loop is inside the PC0-triggered challenge: serial availability and byte reads occur at `0x1030`–`0x1048`. CR or LF submits the line; other bytes are accumulated. The user input is converted to lowercase at `0x1062`–`0x108a` via the routine at `0x2362`, which maps ASCII `A`–`Z` to `a`–`z`. The code trims leading and trailing ASCII whitespace at `0x10f8`–`0x115e`, using the classifier at `0x1e20` (space and tab/line-control characters).

At `0x1094`–`0x10a6`, the firmware copies the sole expected answer literal, `rick astley` from flash `0x27b6`, into a String buffer and records its length as 11. At `0x1166`–`0x1198`, it compares the trimmed input length to 11 and then calls the string comparison routine at `0x2384` once. Only equality reaches the `ACCESS GRANTED` branch at `0x120a`. The other branch prints `ACCESS DENIED` and decrements the three-attempt counter. No other expected-name string or alternate comparison branch was found. Case and outer-whitespace variants of Rick Astley should therefore be accepted; a different full name should not be, barring unintended memory corruption.

## State and alternate triggers

- The application makes seven direct calls to digitalRead at `0x072a`; each uses software pin 13 (SW1) or software pin 10 (PC0). The pin mapping and observed behavior agree. There is no third directly polled input in these calls.
- Startup compares EEPROM `0x1400`–`0x1405` against `GRRE 01 00` at `0x1510`–`0x153e`. If mismatched, the six calls to the EEPROM write helper at `0x1540`–`0x1584` write those exact bytes. These are all direct calls to that helper. No application code was found that records successful answers or advances an EEPROM stage.
- The populated interrupt vectors reach timer bookkeeping and a generic port callback dispatcher. They do not directly print a secret message or read a new EEPROM key. Indirect callbacks still prevent a formal proof of no alternate path.
- Normal and Sentinel loops call the same PC0 challenge routine. After its `System shutdown` text, it sets a RAM flag and returns; the MCU is still running. This fits retriggering the same challenge.
- Sentinel's watch pattern is computed with standard AVR pseudorandom code and contains no direct UART-print path of its own after its startup messages. Normal mode has five LED-animation states selected by short SW1 presses; Sentinel does not read that state.

## Conclusion and limits

The captured firmware provides strong evidence for **one intended accepted identity: Rick Astley**, one PC0 challenge, and no persistent second stage. The second link appears to be the final firmware-produced output. Live SRAM was not dumped; it is volatile and initialized by the captured program at startup. The programmable flash, EEPROM, and User Row have now been captured; no additional clue was found in the User Row or fuses. A hidden algorithmic encoding, external web puzzle, or an unforeseen indirect callback cannot be categorically excluded from static analysis alone. No badge writes or additional hardware connections were made for this audit.
