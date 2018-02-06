"""
Basic utility for seeing address for a given IPv4 address and netmask
"""

def netmask(mask):
    """Convert mask prefix to masks numerical value"""
    ipv4_min, ipv4_max = 0, 32

    if not isinstance(mask, int):
        raise TypeError("Mask must be of type 'int'. Received: %s", mask)
    if mask < ipv4_min or mask > ipv4_max:
        raise ValueError("IPv4 masks must be within range %d <= mask <= %d",
                ipv4_min, ipv4_max)

    return (2 ** mask - 1) << (ipv4_max - mask)

