# Assume:
# A program is a list of integers that represent some type of intcode
# of the shape:
# INSTR arg0 arg1 ...
# Where each INSTR has an INSTR_WIDTH that gives the total width of that
# instruction (minimally 1).
# So if INSTR 0 = MUL, WIDTH 3, then [0,1,5] = MUL 1 5
import utils
from icode.debug import print_debug, pretty_args
from icode.instructions import parse_op, has_op, get_opcode


class interpreter:
    def __init__(self, code):
        self.code = code
        self.original_code = code[:]
        self.__restart_vars()

        self.verbose = False
        self.printer = print_debug
        self.tracing = False
        self.tracing_fn = None
        self.max_iter = -1
        self.debugger = None

    def __restart_vars(self):
        self.ip = 0
        self.relative_base = 0
        self.finished = False
        self.input = []

    def restart(self):
        self.code = self.original_code[:]
        self.__restart_vars()

    def run_until_blocked(self):
        output = []
        self.code, output, self.ip, self.relative_base, self.finished = run(self.code, data_input=self.input, verbose=self.verbose,\
            printer=self.printer, tracing=self.tracing, tracing_fn=self.tracing_fn,
            ip=self.ip, relative_base=self.relative_base, max_iter=self.max_iter, debugger=self.debugger)
        return output, self.finished

    def run(self, input_provider, **kwargs):
        while not self.finished:
            output, finished = self.run_until_blocked()
            if not finished:
                self.input, cont = input_provider(output, **kwargs)
                if not cont:
                    self.finished = True


def run(stream, data_input=[], verbose=False, printer=print_debug, \
    tracing=False, tracing_fn=None, ip=0, relative_base=0, max_iter=-1, debugger=None):

    data = stream if isinstance(stream, utils.longlist) else utils.longlist(stream[:])
    data_output = []

    num_iterations = 0

    while max_iter == -1 or num_iterations < max_iter:
        num_iterations += 1
        old_ip = ip
        op = get_opcode(data[ip])

        if op == 99: 
            return data, data_output, ip, relative_base, True # Magic breaking OP.
        if op == 3 and len(data_input) == 0:
                return data, data_output, ip, relative_base, False # Yield support. 

        if has_op(op):
            op_str = data[ip]
            opcode = parse_op(op_str)
            start_ip = ip

            if opcode.output_arg >= 0:
                args = data[ip:(ip+opcode.width)]
                output_arg = args[opcode.output_arg]
                
                if verbose or tracing: 
                    inputs = pretty_args(data, ip, args, opcode, relative_base)
                    old_rb = relative_base

                if debugger != None:
                    debugger(data, ip, opcode, args, data_input)

                out_data, ip, output_data, new_rb = opcode.eval(data, args, ip, opcode.mode, data_input, relative_base)
                
                if out_data != None: 
                    if opcode.mode[opcode.output_arg-1] == 0:
                        data[output_arg] = out_data
                    else: # Relative base
                        data[relative_base+output_arg] = out_data
                
                if output_data != None: data_output.append(output_data)
                if new_rb      != None: relative_base += new_rb

                if verbose or tracing: 
                    outputs = pretty_args(data, ip, args, opcode, relative_base)
                    if verbose: 
                        print_debug(start_ip, op_str, opcode, args, inputs, outputs, old_rb, relative_base)
                    if tracing: 
                        tracing_fn(start_ip, opcode, args, inputs, outputs)

            if old_ip == ip:
                ip += opcode.width
        else:
            ip += 1
    return data, data_output, ip, relative_base, True

