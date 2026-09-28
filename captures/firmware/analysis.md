# Firmware analysis: control-flow and LED review

Source: two matching read-only ATtiny1616 flash captures and two matching EEPROM captures in this directory. Address offsets below are byte offsets in `attiny1616-flash-1.bin`; the analysis is from AVR disassembly and is still in progress.

## Findings supported by code

- Startup compares EEPROM locations `0x1400`–`0x1405` with `47 52 52 45 01 00` (`GRRE\x01\x00`) around code address `0x1510`. If they differ, it writes those six bytes. The observed EEPROM value is therefore the firmware's initialization marker, not evidence of an unlocked challenge stage.
- At `0x1592`–`0x1598`, a digital-pin read chooses the Sentinel branch versus normal operation. The [ATtiny1616 megaTinyCore pin mapping](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/variants/txy6/pins_arduino.h) maps digital 13 to PC3, consistent with the SW1 startup observation.
- The five values printed as `ledPins` are stored literally as 16-bit values at flash `0x23d8`: `16, 0, 1, 8, 9`. They are the configured LED pin list. The same pin mapping maps them to PA3, PA4, PA5, PB1, PB0.
- The Sentinel code prints the test/watch messages and enters an LED/watch loop around `0x164a`. After those banner messages there are no further direct UART-print calls in that loop's block. A shared input handler is still called while the loop runs.
- Both Sentinel and normal LED loops call the same handler at `0x1270`, which calls `0x0d24`. That handler reads digital pin 10, mapped to PC0. This accounts for PC0 launching the Rick Astley challenge in either mode.
- The challenge prints `System shutdown`, sets a RAM flag, then returns at `0x126e`. It does not actually halt or remove power. The user's observation that PC0 can retrigger the challenge without a power cycle agrees with this.
- The firmware contains one plain-text `rick astley` answer literal and the two previously observed bit.ly links. No other plain-text prompt or URL was found in the captured flash.

## Sentinel, SW1, and LED patterns

- The Sentinel LED loop at `0x1630`–`0x1972` calls the routine at `0x1d76` repeatedly. Its constants `123459876` (default seed), `127773`, `16807`, and `2836` identify the standard [avr-libc Park–Miller `random()` implementation](https://github.com/avrdudes/avr-libc/blob/main/libc/stdlib/random.c). Startup at `0x14d4`–`0x150e` also seeds this state from a peripheral reading when nonzero. Thus the watch sequence is generated at runtime; it is not simply replaying a fixed LED bitstream from a table. This does **not** prove that no information can be encoded in its algorithm.
- The Sentinel loop uses `random() % 5` to select among the five configured LED pins (`0x1630`–`0x166e`) and additional pseudorandom calls to choose neighboring pins, brightness, and delays (`0x1670`–`0x1972`). This agrees with the observed adjacent groups and variable-looking pattern. We have not reconstructed every timing and brightness calculation.
- The shared SW1 handler at `0x0bf0` reads software pin 13, compares elapsed time against `0x07d1` (2001 ms), and routes a long hold to the display/sleep routine at `0x0a56`. On a short press, it increments the state at RAM `0x388d`–`0x388e` modulo five (`0x0cac`–`0x0ccc`). The normal-mode loop at `0x1a56` branches on states 0–4 and calls different LED routines. The Sentinel LED loop has no read of that state, explaining why short presses change normal animations but have no visible effect in Sentinel. The common long-hold path accounts for both modes' similar observed response.
- The same shared handler at `0x1270` polls SW1 and PC0 in both modes. It can transfer control from Sentinel's LED loop to the normal section at `0x1974` when it reports an event. The exact wake/sleep and transition sequence after a long hold has not been verified on hardware, so the observed LED change should not be described as a proven mode switch.
- The short data region at `0x23ce`–`0x23e1` consists of indices 0–4 and the five LED pin numbers. Later bytes at `0x23e2`–`0x242c` contain small masks/indices and are followed immediately by ordinary text strings. They are not evidence of a prerecorded Sentinel message; the visible Sentinel LED code makes pseudorandom choices directly. Their full use outside Sentinel has not been established.

## What this does not establish

This is not a proof that the badge has no other behavior. Indirect calls, timer-driven LED patterns, and encoded data have not been exhaustively ruled out. The current evidence gives Sentinel an ordinary role as a hardware self-test plus pseudorandom LED watch, rather than a demonstrated second challenge. No more soldering or button-guessing is needed to resolve the remaining static-analysis questions.
