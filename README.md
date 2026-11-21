# AT24C32 for MicroPython

MIT-licensed driver for the AT24C32 32-Kbit (4 KiB) I²C EEPROM. It is
independent of the [DS3231 clock driver](https://github.com/mattytrentini/micropython-ds3231),
even when both chips are on the same module.

## Install

```sh
mpremote mip install github:mattytrentini/micropython-at24c32
```

On a network-connected board:

```python
import mip
mip.install("github:mattytrentini/micropython-at24c32")
```

## Use

Pass an initialized `machine.I2C` or `machine.SoftI2C` bus. The EEPROM uses
`0x50`–`0x57`, depending on its address straps. Some DS3231 modules use `0x57`
for the EEPROM; check your board or use `i2c.scan()`. For writes, the hardware
write-protect pin must be low.

```python
from at24c32 import AT24C32

eeprom = AT24C32(i2c, addr=0x57)
print(eeprom.read(0, 8))

buf = bytearray(8)
eeprom.readinto(0, buf)
# This overwrites EEPROM offsets 30–33, spanning two pages:
eeprom.write(30, b"demo")
```

Offsets are byte offsets from 0 to 4095. `write()` accepts `bytes` or
`bytearray`; `readinto()` accepts a `bytearray`.
Reads and writes cannot wrap the end of memory. `write()` waits for each
32-byte page's write cycle to finish before continuing or returning.
The bus must support 16-bit memory addresses (`addrsize=16`).

Reference: [Microchip AT24C32D datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/AT24C32D-I2C-Compatible-Serial-EEPROM-Data-Sheet-20006047A.pdf).
