import math

def hex_to_bin(string):
    """Converts a string representing a hexadecimal number into a string
    representing the same number in binary.
    """
    # Add an initial 1 at first so as not to lose leading zeros
    return bin(int('1' + string, 16))[3:]

def parse_literal(packet):
    """Parses initial segment of packet (binary string) as a literal value. Returns
    a tuple containing its value (int) and the remainder of the packet (string).
    The packet should not have a prefix.
    """
    bin_value = ""
    last_four_bits = 1
    while last_four_bits:
        last_four_bits = int(packet[0])
        bin_value += packet[1:5]
        packet = packet[5:]
    value = int(bin_value, 2)
    # Remove trailing zeroes
    if packet and int(packet, 2) == 0:
        packet = ""
    return value, packet

def parse(packet):
    """Parses initial segment of packet (binary string) as BITS code, and returns
    parser output and remainder. If packet contains a literal value, parser output
    is the tuple of ints (version, typeID (=4), value). If packet contains an
    operator, parser output is a list with 0th element (version, typeID) and later
    elements the parser output of each subpacket."""
    # print(f"Starting to parse {packet}.")
    if int(packet, 2) == 0:
        # This was an empty packet
        return None
    version = int(packet[0:3], 2)
    typeID = int(packet[3:6], 2)
    packet = packet[6:]
    if typeID == 4:
        # literal value
        value, remainder = parse_literal(packet)
        # print(f"Reading a literal value, version = {version}, typeID = {typeID}, "
        #       + f"value = {value}.")
        # print(f"Remainder to parse: {remainder}.")
        return (version, typeID, value), remainder
    else:
        # operator packet
        output = [(version, typeID)]
        # next bit is length type ID
        length_typeID = int(packet[0], 2)
        packet = packet[1:]
        # print(f"Reading an operator packet, version = {version}, typeID = {typeID}, "
        #       + f"length typeID = {length_typeID}.")
        if length_typeID:
            # next 11 bits are number of subpackets to parse
            num_subpackets = int(packet[0:11], 2)
            packet = packet[11:]
            # print(f"I need {num_subpackets} packets from {packet}.")
            for i in range(num_subpackets):
                # print(f"Subpacket #{i}:")
                sub_parsed, remainder = parse(packet)
                output.append(sub_parsed)
                packet = remainder
            # print(f"Remainder to parse: {remainder}.")
            return output, remainder
        else:
            # next 15 bits are length of subpackets to parse
            length_subpackets = int(packet[0:15], 2)
            packet = packet[15:]
            # print(f"I need {length_subpackets} bits worth of subpackets from {packet}.")
            remainder = packet
            while len(packet) - len(remainder) < length_subpackets:
                # print(f"Next subpacket:")
                sub_parsed, remainder = parse(remainder)
                output.append(sub_parsed)
                # print(f"I've used {len(packet) - len(remainder)} bits.")
            # print(f"Remainder to parse: {remainder}.")
            return output, remainder

def version_sum(packets):
    """packets is BITS parser output, documented in the parse() function. Returns
    the sum of all version numbers appearing in packets.
    """
    if type(packets) is tuple:
        return packets[0]
    elif type(packets) is list:
        return sum([version_sum(p) for p in packets])
    else:
        raise TypeError

def calc_value(code):
    """Calculates the value of parsed BITS code."""
    if type(code) is tuple:
        # must be literal
        assert code[1] == 4
        return code[2]
    assert type(code) is list
    op = code[0][1]
    if op == 0: # sum
        return sum([calc_value(packet) for packet in code[1:]])
    elif op == 1: # product
        return math.prod([calc_value(packet) for packet in code[1:]])
    elif op == 2: # minimum
        return min([calc_value(packet) for packet in code[1:]])
    elif op == 3: # maximum
        return max([calc_value(packet) for packet in code[1:]])
    elif op == 5: # >
        return int(calc_value(code[1]) > calc_value(code[2]))
    elif op == 6: # <
        return int(calc_value(code[1]) < calc_value(code[2]))
    elif op == 7: # ==
        return int(calc_value(code[1]) == calc_value(code[2]))

def test():
    lines = open("test16.txt").read().split("\n")[:-1]
    for x, line in enumerate(lines[7:]):
        print("Test line:", x+7)
        parsed, remainder = parse(hex_to_bin(line))
        if remainder:
            print("Remainder:", remainder)
        print("Version sum:", version_sum(parsed))
        print("Calculated value:", calc_value(parsed))

def prob16a():
    hex_data = open("input16.txt").read().replace("\n", "")
    bin_data = hex_to_bin(hex_data)
    parsed, remainder = parse(bin_data)
    if remainder:
        print("Remainder:", remainder)
    print(version_sum(parsed))

def prob16b():
    hex_data = open("input16.txt").read().replace("\n", "")
    bin_data = hex_to_bin(hex_data)
    parsed, remainder = parse(bin_data)
    if remainder:
        print("Remainder:", remainder)
    print(calc_value(parsed))

if __name__ == "__main__":
    prob16b()
