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
