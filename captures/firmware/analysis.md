# Firmware analysis: first control-flow pass

Source: two matching read-only ATtiny1616 flash captures and two matching EEPROM captures in this directory. Address offsets below are byte offsets in `attiny1616-flash-1.bin`; the analysis is from AVR disassembly and is still in progress.

## Findings supported by code

- Startup compares EEPROM locations `0x1400`–`0x1405` with `47 52 52 45 01 00` (`GRRE\x01\x00`) around code address `0x1510`. If they differ, it writes those six bytes. The observed EEPROM value is therefore the firmware's initialization marker, not evidence of an unlocked challenge stage.
- At `0x1592`–`0x1598`, a digital-pin read chooses the Sentinel branch versus normal operation. The [ATtiny1616 megaTinyCore pin mapping](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/variants/txy6/pins_arduino.h) maps digital 13 to PC3, consistent with the SW1 startup observation.
- The five values printed as `ledPins` are stored literally as 16-bit values at flash `0x23d8`: `16, 0, 1, 8, 9`. They are the configured LED pin list. The same pin mapping maps them to PA3, PA4, PA5, PB1, PB0.
- The Sentinel code prints the test/watch messages and enters an LED/watch loop around `0x164a`. After those banner messages there are no further direct UART-print calls in that loop's block. A shared input handler is still called while the loop runs.
- Both Sentinel and normal LED loops call the same handler at `0x1270`, which calls `0x0d24`. That handler reads digital pin 10, mapped to PC0. This accounts for PC0 launching the Rick Astley challenge in either mode.
- The challenge prints `System shutdown`, sets a RAM flag, then returns at `0x126e`. It does not actually halt or remove power. The user's observation that PC0 can retrigger the challenge without a power cycle agrees with this.
- The firmware contains one plain-text `rick astley` answer literal and the two previously observed bit.ly links. No other plain-text prompt or URL was found in the captured flash.

## What this does not establish

This is not a proof that the badge has no other behavior. Indirect calls, timer-driven LED patterns, encoded data, and every button state path have not yet been fully traced. The LED pattern tables near `0x23e2`–`0x242c` are the next useful offline target. No more soldering or button-guessing is needed for that analysis.
