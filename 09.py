import interp
import utils 
import sys

has_written = set()

def debugger(code, ip, opcode, args, data_input):
    None
    if ip == 928:
        if not code.last_written in has_written:
            print(code.last_written)
            has_written.add(code.last_written)

stream = utils.read_input()
output = []
interp.run(stream, data_input=[1], data_output=output, verbose=True)
interp.run(stream, data_input=[2], data_output=output)
print(output)