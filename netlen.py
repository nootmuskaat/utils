#!/usr/bin/python
"""
Basic utility for seeing address for a given IPv4 address and netmask
"""
import argparse

BYTE_SIZE = 8
BYTE_MIN_SIZE = 0
BYTE_MAX_SIZE = 2**BYTE_SIZE - 1

IPV4_ADDR_LEN = 4
IPV4_MIN_LEN = 0
IPV4_MAX_LEN = BYTE_SIZE * IPV4_ADDR_LEN
IPV4_MIN_VAL = 0
IPV4_MAX_VAL = 2**IPV4_MAX_LEN - 1

def netmask(mask):
    """Convert mask prefix to masks numerical value"""
    if not isinstance(mask, int):
        raise TypeError("mask must be of type 'int'. Received: {}".format(mask))
    if mask < IPV4_MIN_LEN or mask > IPV4_MAX_LEN:
        raise ValueError("mask not within range")

    return (2 ** mask - 1) << (IPV4_MAX_LEN - mask)

def ipaddr(address):
    """Convert IP address to its numerical value"""
    if not isinstance(address, str):
        raise TypeError("address must be of type 'str'. Received {}".format(
            address))
    # raises ValueError if int not found
    addr_bytes = [int(byte) for byte in address.split(".")]
    if len(addr_bytes) != IPV4_ADDR_LEN:
        raise ValueError("invalid address length")
    for byte in addr_bytes:
        if byte < BYTE_MIN_SIZE or byte > BYTE_MAX_SIZE:
            raise ValueError("invalid address element '{}'".format(byte))

    base = 0
    for byte in addr_bytes[:-1]:
        base += byte
        base <<= BYTE_SIZE
    base += addr_bytes[-1]

    return base

def to_address(addr_int):
    """Convert from address' numerical value to human readable form"""
    if not isinstance(addr_int, int):
        raise TypeError("input must be of type 'int'")
    if addr_int < IPV4_MIN_VAL or addr_int > IPV4_MAX_VAL:
        raise ValueError("input not within IPv4 address range")

    addr_bytes = []
    for _ in range(4):
        addr_bytes.append(addr_int & BYTE_MAX_SIZE)
        addr_int >>= BYTE_SIZE

    return ".".join([str(byte) for byte in addr_bytes[::-1]])

def lower(address, mask):
    """Return lower bound of the given subnet"""
    address = ipaddr(address)
    mask = netmask(mask)
    return to_address(address & mask)

def upper(address, mask):
    """Return upper bound of the given subnet"""
    tail = IPV4_MAX_LEN - mask

    address = ipaddr(address)
    mask = netmask(mask)

    return to_address((address & mask) + (2**tail - 1))

def _cliargs():
    """Return CLI args as tuple (address, netmask)"""
    parser = argparse.ArgumentParser()
    parser.add_argument("address", type=str,
            help="An IPv4 address, eg 127.0.0.1")
    parser.add_argument("netmask", type=int,
            help="An IPv4 CIDR prefix, eg 24 for /24 (255.255.255.0)")
    args = parser.parse_args()
    return (args.address, args.netmask)

def main():
    """Run with CLI parameters"""
    addr, nmask = _cliargs()
    try:
        print("{} - {}".format(
            lower(addr, nmask), upper(addr, nmask)
            ))
    except (ValueError, TypeError) as exc:
        print("ERROR: {}".format(exc))
        return 1

    return 0

if __name__ == "__main__":
    main()
