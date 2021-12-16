from solutions.get_inputs import read_inputs


HEX_MAP = {i.split(' = ')[0].strip(): i.split(' = ')[1].strip() for i in """
0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
""".strip().split('\n')}


class Parser:

    def __init__(self, line):
        self.orig_line = line.strip()
        self.packets = None

    def parse(self):
        if self.packets is not None:
            raise Exception()
        self.packets = []
        remaining = list(self.orig_line)
        while len(remaining) > 11:
            packet = Packet(remaining)
            remaining = remaining[packet.length:]
            self.packets.append(packet)

    def evaluate(self):
        if self.packets is None or len(self.packets) != 1:
            raise Exception("Broken assumption that there is only one packet after parsing")
        return self.packets[0].evaluate()

    def unwrap_packets(self):
        queue = [p for p in self.packets]
        result = []
        while queue:
            next = queue.pop()
            result.append(next)
            queue += [p for p in next.sub_packets]
        return result


class Packet:

    def __init__(self, bits):
        self.version = ''.join(bits[:3])
        self.type = ''.join(bits[3:6])
        self.sub_packets = []
        self.length = None
        self.literal_value = None
        self._parse(bits)

    def version_int(self):
        return _binary_to_decimal(self.version)

    def type_int(self):
        return _binary_to_decimal(self.type)

    def literal_int(self):
        return _binary_to_decimal(self.literal_value)

    def evaluate(self):
        type_int = self.type_int()
        if type_int == 4:
            if self.literal_value is None:
                raise Exception()
            return self.literal_int()
        elif type_int == 0:
            return sum(p.evaluate() for p in self.sub_packets)
        elif type_int == 1:
            result = self.sub_packets[0].evaluate()
            if len(self.sub_packets) < 2:
                return result
            for packet in self.sub_packets[1:]:
                result *= packet.evaluate()
            return result
        elif type_int == 2:
            return min(p.evaluate() for p in self.sub_packets)
        elif type_int == 3:
            return max(p.evaluate() for p in self.sub_packets)
        elif type_int == 5:
            if len(self.sub_packets) != 2:
                raise Exception()
            return 1 if self.sub_packets[0].evaluate() > self.sub_packets[1].evaluate() else 0
        elif type_int == 6:
            if len(self.sub_packets) != 2:
                raise Exception()
            return 1 if self.sub_packets[0].evaluate() < self.sub_packets[1].evaluate() else 0
        elif type_int == 7:
            if len(self.sub_packets) != 2:
                raise Exception()
            return 1 if self.sub_packets[0].evaluate() == self.sub_packets[1].evaluate() else 0

    def _parse(self, bits):
        if self.type == '100':
            length, value = self._parse_literal(bits[6:])
            self.length = 6 + length
            self.literal_value = value
        else:
            length, sub_packets = self._parse_operator(bits[6:])
            self.length = 6 + length
            self.sub_packets = sub_packets

    def _parse_literal(self, bits):
        chunks = []
        last = False
        i = 0
        while not last:
            if bits[i] == '0':
                last = True
            chunks.append(''.join(bits[i+1:i+5]))
            i += 5
        return i, ''.join(chunks)

    def _parse_operator(self, bits):
        length_type_id = bits[0]
        if length_type_id == '0':
            length, sub_packets = self._parse_0_operator(bits)
        elif length_type_id == '1':
            length, sub_packets = self._parse_1_operator(bits)
        else:
            raise Exception('Unrecognized ltid ' + length_type_id)
        return length, sub_packets

    def _parse_0_operator(self, bits):
        length_of_subpackets = _binary_to_decimal(''.join(bits[1:16]))
        sub_packets = []
        i = 16
        while i < 16 + length_of_subpackets:
            packet = Packet(bits[i:])
            i += packet.length
            sub_packets.append(packet)
        return i, sub_packets

    def _parse_1_operator(self, bits):
        num_subpackets = _binary_to_decimal(''.join(bits[1:12]))
        sub_packets = []
        i = 12
        while len(sub_packets) < num_subpackets:
            packet = Packet(bits[i:])
            i += packet.length
            sub_packets.append(packet)
        return i, sub_packets

    def __repr__(self):
        return f"Packet[version_int={self.version_int()} type_int={self.type_int()} length={self.length} value={self.literal_value} num_subpackets={len(self.sub_packets)}]"



def run_1(inputs):
    line = inputs[0].strip()
    return _get_version_sum(line)


def run_2(inputs):
    line = inputs[0].strip()
    return _evaluate_line(line)


def _evaluate_line(line):
    binary = _convert_to_binary(line)
    parser = Parser(binary)
    parser.parse()
    return parser.evaluate()


def _get_version_sum(line):
    binary = _convert_to_binary(line)
    parser = Parser(binary)
    parser.parse()
    all_packets = parser.unwrap_packets()
    return sum(p.version_int() for p in all_packets)


def _convert_to_binary(line):
    return "".join([HEX_MAP[i] for i in line])


def _binary_to_decimal(binary_string):
    return int(binary_string, 2)


def run_tests():

    if _binary_to_decimal('011111100101') != 2021:
        raise Exception()

    if _convert_to_binary('D2FE28') != '110100101111111000101000':
        raise Exception()

    if _get_version_sum('D2FE28') != 6:
        raise Exception()

    if _get_version_sum('38006F45291200') != 9:
        raise Exception()

    if _get_version_sum('8A004A801A8002F478') != 16:
        raise Exception()

    if _get_version_sum('620080001611562C8802118E34') != 12:
        raise Exception()

    if _get_version_sum('C0015000016115A2E0802F182340') != 23:
        raise Exception()

    if _get_version_sum('A0016C880162017C3686B18A3D4780') != 31:
        raise Exception()

    if _evaluate_line('C200B40A82') != 3:
        raise Exception()

    if _evaluate_line('04005AC33890') != 54:
        raise Exception()

    if _evaluate_line('880086C3E88112') != 7:
        raise Exception()

    if _evaluate_line('CE00C43D881120') != 9:
        raise Exception()

    if _evaluate_line('D8005AC2A8F0') != 1:
        raise Exception()

    if _evaluate_line('F600BC2D8F') != 0:
        raise Exception()

    if _evaluate_line('9C005AC2F8F0') != 0:
        raise Exception()

    if _evaluate_line('9C0141080250320F1802104A08') != 1:
        raise Exception()


if __name__ == "__main__":
    run_tests()

    input = read_inputs(16)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
