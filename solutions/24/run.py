from solutions.get_inputs import read_inputs


DEBUG = False


class Program:

    def __init__(self, instructions):
        self.instructions = self._parse_instructions(instructions)

    def _parse_instructions(self, instructions):
        result = []
        for instruction in instructions:
            parts = instruction.strip().split(' ')
            result.append((parts[0], tuple(parts[1:])))
        return result

    def run(self, inputs):
        inputs = [int(i) for i in inputs]
        state = {i: 0 for i in ['x', 'y', 'z', 'w']}
        for command, values in self.instructions:
            if command == 'inp':
                print(state)
                self._do_inp(inputs, state, values)
                if DEBUG: print(f'command: {command} values: {values} state: {state} inputs: {inputs}')
            elif command == 'mul':
                self._do_mul(state, values)
                if DEBUG: print(f'command: {command} values: {values} state: {state} inputs: {inputs}')
            elif command == 'eql':
                self._do_eql(state, values)
                if DEBUG: print(f'command: {command} values: {values} state: {state} inputs: {inputs}')
            elif command == 'add':
                self._do_add(state, values)
                if DEBUG: print(f'command: {command} values: {values} state: {state} inputs: {inputs}')
            elif command == 'div':
                self._do_div(state, values)
                if DEBUG: print(f'command: {command} values: {values} state: {state} inputs: {inputs}')
            elif command == 'mod':
                self._do_mod(state, values)
                if DEBUG: print(f'command: {command} values: {values} state: {state} inputs: {inputs}')
            else:
                raise Exception(command)

        return state

    def _do_inp(self, inputs, state, command_values):
        if not inputs:
            raise Exception("Called for input but none remained")
        assert len(command_values) == 1
        input_value = inputs.pop(0)
        state[command_values[0]] = input_value

    def _do_mul(self, state, command_values):
        left, left_value, right, right_value = self._parse_command_values(state, command_values)
        result = left_value * right_value
        state[left] = result

    def _do_add(self, state, command_values):
        left, left_value, right, right_value = self._parse_command_values(state, command_values)
        result = left_value + right_value

        state[left] = result

    def _do_div(self, state, command_values):
        left, left_value, right, right_value = self._parse_command_values(state, command_values)
        result = int(left_value / right_value)
        state[left] = result

    def _do_mod(self, state, command_values):
        left, left_value, right, right_value = self._parse_command_values(state, command_values)
        result = left_value % right_value
        state[left] = result

    def _do_eql(self, state, command_values):
        left, left_value, right, right_value = self._parse_command_values(state, command_values)
        result = left_value == right_value
        state[left] = 1 if result else 0

    def _parse_command_values(self, state, command_values):
        assert len(command_values) == 2
        left = self._get_var_or_int(command_values[0])
        right = self._get_var_or_int(command_values[1])

        if left not in state:
            raise Exception(f'left {left} not in state {state}')
        if not isinstance(right, int) and right not in state:
            raise Exception(f'right {right} not in state {state}')

        left_value = state[left]
        right_value = right if isinstance(right, int) else state[right]
        return left, left_value, right, right_value

    def _get_var_or_int(self, command_value):
        try:
            return int(command_value)
        except Exception:
            return command_value


    def __repr__(self):
        return str(self.instructions)


def run_tests():
    test_inputs = """
    inp x
    mul x -1
    """.strip().split('\n')
    if Program(test_inputs).run([1])['x'] != -1:
        raise Exception()
    if Program(test_inputs).run([-33])['x'] != 33:
        raise Exception()

    test_inputs = """
    inp z
    inp x
    mul z 3
    eql z x
    """.strip().split('\n')
    if Program(test_inputs).run([2,6])['z'] != 1:
        raise Exception()

    test_inputs = """
    inp w
    add z w
    mod z 2
    div w 2
    add y w
    mod y 2
    div w 2
    add x w
    mod x 2
    div w 2
    mod w 2
    """.strip().split('\n')
    if Program(test_inputs).run([8]) != {'x': 0, 'y': 0, 'z': 0, 'w': 1}:
        raise Exception()
    if Program(test_inputs).run([3]) != {'x': 0, 'y': 1, 'z': 1, 'w': 0}:
        raise Exception()


if __name__ == "__main__":
    run_tests()

    input_data = read_inputs(24)

    program = Program(input_data)
    # Part 1 - this answer was achieved manually in ipython
    result = program.run(list('74929995999389'))
    if result['z'] == 0:
        print('Part 1 passed')

    # Part 2 - this answer was achieved manually in ipython
    result = program.run(list('11118151637112'))
    if result['z'] == 0:
        print('Part 2 passed')
