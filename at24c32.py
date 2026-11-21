# SPDX-License-Identifier: MIT
"""MicroPython driver for the AT24C32 4 KiB I2C EEPROM."""

from time import sleep_ms


class AT24C32:
    CAPACITY = 4096
    PAGE_SIZE = 32

    def __init__(self, i2c, addr=0x50):
        if not 0x50 <= addr <= 0x57:
            raise ValueError("EEPROM I2C address must be 0x50–0x57")
        self.i2c = i2c
        self.addr = addr

    def _check_span(self, offset, length):
        if offset < 0 or length < 0 or offset + length > self.CAPACITY:
            raise ValueError("EEPROM access outside 4096-byte address space")

    def read(self, offset, length=1):
        """Read length bytes starting at offset."""
        self._check_span(offset, length)
        if not length:
            return b""
        return self.i2c.readfrom_mem(self.addr, offset, length, addrsize=16)

    def readinto(self, offset, buf):
        """Read into a bytearray starting at offset."""
        if not isinstance(buf, bytearray):
            raise TypeError("buf must be a bytearray")
        length = len(buf)
        self._check_span(offset, length)
        if length:
            self.i2c.readfrom_mem_into(self.addr, offset, buf, addrsize=16)

    def write(self, offset, data):
        """Write bytes or a bytearray without crossing a page in one transfer."""
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or bytearray")
        data = memoryview(data)
        length = len(data)
        self._check_span(offset, length)
        start = 0
        while start < length:
            size = min(self.PAGE_SIZE - offset % self.PAGE_SIZE, length - start)
            self.i2c.writeto_mem(self.addr, offset, data[start : start + size], addrsize=16)
            # The chip will not accept another command during its write cycle.
            sleep_ms(5)
            start += size
            offset += size
