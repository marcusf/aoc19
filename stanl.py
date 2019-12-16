from icode.parser import parse
from icode.debug import pretty_code, pretty_dummy, style
from utils import read_input
from prompt_toolkit import print_formatted_text, HTML


stream = read_input(fname='13.input')

code, mapping = parse(stream)

def analyse_rels(code):
    possibles = []
    fns = dict()
    for i, (loc, op, args) in enumerate(code):
        if op.name == 'rel' and op.mode[0] == 1:
            possibles.append((i, loc, op, args[1]))
    
    for p1,p2 in zip(possibles,possibles[1:]):
        i1, loc1, _, o1 = p1
        i2, loc2, _, o2 = p2
        if o2 == -o1 and o1 > 0:
            fns[loc1] = ((i1,i2),(loc1,loc2+1))
    return fns
    
def find_callers(fn, code):
    (l1, l2), (loc1, loc2)  = fn
    callers = []

    for i, (loc, op, args) in enumerate(code):
        # Conditional function call
        if (op.name == 'jnz' or op.name == 'jz') and args[2] == loc1:
            callers.append((i,loc))
    #print(loc1)
    return callers

def simplify_and_print(code, fns):
    for i, (loc, op, args) in enumerate(code):

        code, extra = '', ''

        # Detect unconditional jumps and potential function calls
        if (op.name == 'jnz' and op.mode[0] == 1 and args[1] != 0) or \
            (op.name == 'jz' and op.mode[0] == 1 and args[1] == 0):
            code = pretty_dummy(loc, 'jmp', modes=op.mode[1:], width=2, args=[0,args[2]], operator='')
            if op.mode[1] == 1 and args[2] in fns:
                extra = f'<opt>; Likely call to function at {args[2]}</opt>'

        # Simplify add and mul of two constants
        elif op.name == 'mul' and op.mode[0] == 1 and op.mode[1] == 1:
            code = pretty_dummy(loc, 'set (mul)', modes=[1,op.mode[2]], width=3, args=[0,args[1]*args[2],args[3]],operator='=')
        elif op.name == 'add' and op.mode[0] == 1 and op.mode[1] == 1:
            code = pretty_dummy(loc, 'set (add)', modes=[1,op.mode[2]], width=3, args=[0,args[1]+args[2],args[3]],operator='=')

        # Simplify if mul or add with (1,0) on one parameter
        elif (op.name == 'mul' and (op.mode[0] == 1 and args[1] == 1)) or \
                (op.name == 'add' and (op.mode[0] == 1 and args[1] == 0)):
            pretty_dummy(loc, 'set (muladd)', modes=[op.mode[1],op.mode[2]], width=3, args=[0,args[2],args[3]],operator='=')

        elif (op.name == 'mul' and (op.mode[1] == 1 and args[2] == 1)) or \
                (op.name == 'add' and (op.mode[1] == 1 and args[2] == 0)):
            pretty_dummy(loc, 'set (muladd)', modes=[op.mode[0],op.mode[2]], width=3, args=[0,args[1],args[3]],operator='=')


        # Annotate for functions
        elif loc in fns:
            print('')
            code = pretty_dummy(loc, 'function_start (REL), args =', modes=op.mode, width=2, args=[0,args[1]], operator='()')
        else:
            code = pretty_code(loc, op, args)

        print_formatted_text(HTML(code+extra), style=style)

fns = analyse_rels(code)
#for fn in fns:
#    print(fn, find_callers(fn, code))

simplify_and_print(code, fns)

#print(code[mapping[10]])