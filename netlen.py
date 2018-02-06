"""
Basic utility for seeing address for a given IPv4 address and netmask
"""

def netmask(mask):
    """Convert mask prefix to masks numerical value"""
    ipv4_min, ipv4_max = 0, 32

    if not isinstance(mask, int):
        raise TypeError("mask must be of type 'int'. Received: {}".format(mask))
    if mask < ipv4_min or mask > ipv4_max:
        raise ValueError(
            "IPv4 masks must be within range {} <= mask <= {}".format(
                ipv4_min, ipv4_max))

    return (2 ** mask - 1) << (ipv4_max - mask)

def ipaddr(address):
    """Convert IP address to its numerical value"""
    ipv4_min, ipv4_max = 0, 255
    ipv4_addr_len = 4
    byte_len = 8

    if not isinstance(address, str):
        raise TypeError("address must be of type 'str'. Received {}".format(
            address))
    # raises ValueError if int not found
    addr_bytes = [int(byte) for byte in address.split(".")]
    if len(addr_bytes) != ipv4_addr_len:
        raise ValueError("Invalid address length")
    for byte in addr_bytes:
        if byte < ipv4_min or byte > ipv4_max:
            raise ValueError("Invalid address element '{}'".format(byte))

    base = 0
    for byte in addr_bytes[:-1]:
        base += byte
        base <<= byte_len
    base += addr_bytes[-1]

    return base

def to_address(addr_int):
    """Convert from address' numerical value to human readable form"""
    ipv4_min, ipv4_max = 0, 2**32 - 1
    if not isinstance(addr_int, int):
        raise TypeError("Input must be of type 'int'")
    if addr_int < ipv4_min or addr_int > ipv4_max:
        raise ValueError("Input not within IPv4 address range")

    byte = 2**8 - 1
    byte_len = 8

    addr_bytes = []
    for _ in range(4):
        addr_bytes.append(addr_int & byte)
        addr_int >>= byte_len

    return ".".join([str(byte) for byte in addr_bytes[::-1]])

def lower(address, mask):
    """Return lower bound of the given subnet"""
    address = ipaddr(address)
    mask = netmask(mask)
    return to_address(address & mask)

def upper(address, mask):
    """Return upper bound of the given subnet"""
    ipv4_max = 32
    tail = ipv4_max - mask

    address = ipaddr(address)
    mask = netmask(mask)

    return to_address((address & mask) + (2**tail - 1))
