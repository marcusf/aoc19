import interp
import utils
import sys
import asyncio

from prompt_toolkit import prompt, print_formatted_text, HTML, prompt, PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

from icode.debug import print_debug, pretty_code, style

trace_log = []

def tracer(loc, opcode, args, inputs, outputs):
    trace_log.append((loc,opcode,args,inputs,outputs))

def run(stream, debug=False, trace=False,input_data=[],ip=0):
    _, output, ip, terminated = interp.run(stream, debug=debug, printer=print_debug,\
         tracing=trace, tracing_fn=tracer, data_input=input_data)
    print(f'output={output}; terminated={terminated}, ip={ip}')
    return ip

stream = None
fname = ''
pokes = []
input_data = []
ip = 0

def cli_load(args):
    global stream
    global fname
    fname = args[0]
    try:
        stream = utils.read_input(fname=fname)
        print(f'loaded {fname}')
    except:
        print(f'unable to load {fname}')

def cli_continue(args):
    global stream
    global input_data
    global ip
    verbose = 'verbose' in args
    trace = 'trace' in args
    print(f'executing {fname}, verbose={verbose}, trace={trace} from ip={ip}')
    ip = run(stream, verbose, trace, input_data,ip=ip)

def cli_run(args):
    global stream
    global input_data
    global ip
    verbose = 'verbose' in args
    trace = 'trace' in args
    print(f'executing {fname}, verbose={verbose}, trace={trace}')
    ip = run(stream, verbose, trace, input_data, ip=0)

def cli_print(args):
    global stream
    program, _ = interp.parse(stream)
    for row in program:
        print_formatted_text(HTML(pretty_code(*row)), style=style)

def cli_poke(args):
    global stream
    global pokes
    pos, val = int(args[0]), int(args[1])
    stream[pos] = val
    pokes.append(f'{pos}={val}')
    print(f'Updating {fname}, position {pos} = {val}')

def cli_exit(args):
    sys.exit(1)

def cli_data(args):
    global input_data
    for arg in args:
        input_data.append(int(arg))

commands = {'load':  {'argc': [1],          'fn': cli_load},
            'run':   {'argc': [0,1,2],      'fn': cli_run},
            'print': {'argc': [0],          'fn': cli_print},
            'poke':  {'argc': [2],          'fn': cli_poke},
            'exit':  {'argc': [0],          'fn': cli_exit},
            'continue':  {'argc': [0,1,2],  'fn': cli_continue},
            'input':  {'argc': [1,2,3,4,5,6,7,8,9,10], 'fn': cli_data}}

if __name__ == '__main__':
    clist = list(commands.keys())
    command_completer = WordCompleter(clist)
    cli_history = FileHistory(".clihistory")
    session = PromptSession(history=cli_history)

    try:
        while True:
            bname = fname if len(fname)>0 else 'no file loaded'
            pokess = ", pokes: (" + ", ".join(pokes) + ")" if len(pokes) > 0 else ''
            bottom = f' {bname} {pokess}, input={input_data}, ip={ip}'
            text = session.prompt('> ', completer=command_completer, complete_while_typing=False,  bottom_toolbar=bottom)
            command = text.strip().split(' ')
            if len(command) == 0 or len(text) == 0: 
                continue
            op = command[0]
            if op in clist:
                argv = command[1:]
                if len(argv) in commands[op]['argc']:
                    commands[op]['fn'](argv)
                else:
                    argl = ', '.join([str(s) for s in commands[op]['argc']])
                    largv = len(argv)
                    print(f'expected {argl} arguments, got {largv}')
            else:
                print(f'unexpected command {command}')

    except KeyboardInterrupt:
        sys.exit(0)
            

    

