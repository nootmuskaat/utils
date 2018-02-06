"""
Tests for netlen.py
"""
import unittest

import netlen

FOUR_BYTE_MIN = (2**0) - 1
FOUR_BYTE_MAX = (2**32) - 1

class TestNetMask(unittest.TestCase):
    def test_input(self):
        with self.assertRaises(TypeError):
            netlen.netmask("dog")
        with self.assertRaises(TypeError):
            netlen.netmask(24.5)
        with self.assertRaises(ValueError):
            netlen.netmask(-1)
        with self.assertRaises(ValueError):
            netlen.netmask(33)

    def test_values(self):
        self.assertEqual(netlen.netmask(0), FOUR_BYTE_MIN)
        self.assertEqual(netlen.netmask(32), FOUR_BYTE_MAX)
        self.assertEqual(netlen.netmask(8),  0b11111111000000000000000000000000)
        self.assertEqual(netlen.netmask(23), 0b11111111111111111111111000000000)

class TestIPAddress(unittest.TestCase):
    def test_ipaddr_input(self):
        with self.assertRaises(TypeError):
            netlen.ipaddr(75)
        with self.assertRaises(TypeError):
            netlen.ipaddr([10, 10, 10, 10])
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10.1O")
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10.666")
        with self.assertRaises(ValueError):
            netlen.ipaddr("-10.10.10.66")
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10")
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10.10.10")

    def test_ipaddr_values(self):
        self.assertEqual(netlen.ipaddr("0.0.0.0"), FOUR_BYTE_MIN)
        self.assertEqual(netlen.ipaddr("255.255.255.255"), FOUR_BYTE_MAX)
        self.assertEqual(netlen.ipaddr("10.10.10.10"),
                         0b00001010000010100000101000001010)

    def test_reverse_input(self):
        with self.assertRaises(TypeError):
            netlen.to_address("10000000")
        with self.assertRaises(ValueError):
            netlen.to_address(-1)
        with self.assertRaises(ValueError):
            netlen.to_address(2**32)

    def test_reverse_values(self):
        self.assertEqual(netlen.to_address(FOUR_BYTE_MIN), "0.0.0.0")
        self.assertEqual(netlen.to_address(FOUR_BYTE_MAX), "255.255.255.255")
        self.assertEqual(netlen.to_address(0b00001010000010100000101000001010),
                "10.10.10.10")

class TestMinMax(unittest.TestCase):
    def test_min(self):
        self.assertEqual(netlen.lower("10.10.10.10", 24), "10.10.10.0")
        self.assertEqual(netlen.lower("10.10.10.10", 30), "10.10.10.8")
        self.assertEqual(netlen.lower("10.10.10.10", 16), "10.10.0.0")

    def test_max(self):
        self.assertEqual(netlen.upper("10.10.10.10", 24), "10.10.10.255")
        self.assertEqual(netlen.upper("10.10.10.10", 30), "10.10.10.11")
        self.assertEqual(netlen.upper("10.10.10.10", 16), "10.10.255.255")

if __name__ == "__main__":
    unittest.main()
