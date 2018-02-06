"""
Tests for netlen.py
"""
import netlen
import unittest

class TestNetMask(unittest.TestCase):
    def test_range(self):
        with self.assertRaises(TypeError):
            netlen.netmask("dog")
        with self.assertRaises(TypeError):
            netlen.netmask(24.5)
        with self.assertRaises(ValueError):
            netlen.netmask(-1)
        with self.assertRaises(ValueError):
            netlen.netmask(33)

    def test_values(self):
        four_byte_min = (2**0) - 1
        four_byte_max = (2**32) - 1
        self.assertEqual(netlen.netmask(0), four_byte_min)
        self.assertEqual(netlen.netmask(32), four_byte_max) 
        self.assertEqual(netlen.netmask(8),  0b11111111000000000000000000000000)
        self.assertEqual(netlen.netmask(23), 0b11111111111111111111111000000000)

class TestIPAddress(unittest.TestCase):
    def test_input(self):
        with self.assertRaises(TypeError):
            netlen.ipaddr(75)
        with self.assertRaises(TypeError):
            netlen.ipaddr([10, 10, 10, 10])
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10.666")
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10")
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10.10.10")
        with self.assertRaises(ValueError):
            netlen.ipaddr("10.10.10.1O")




if __name__ == "__main__":
    unittest.main()
