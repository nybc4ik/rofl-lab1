# Online Python - IDE, Editor, Compiler, Interpreter
import re
from sympy import simplify as sympy_simplify, expand, Symbol
from z3 import *

'''
  The simplify_expression function simplifies expressions. 
  Multiplication must be entered with an asterisk '*'.
  Exponentiation can be implemented as both x**2 and x^2. 
  However, it's important to note that 2^4*5 will be simplified to 80. 
  So, if an expression is in the exponent, it must be enclosed in parentheses '()'.
'''
def simplify_expression(expression):
    # Replace variables with SymPy symbols
    expression = re.sub(r'([a-z]+)', r'Symbol("\1")', expression)

    simplified_expression = expand(sympy_simplify(expression))
    return str(simplified_expression)


'''
  The to_prefix_notation function rewrites an expression in prefix notation. 
  It also creates a set of variables contained in the resulting expression.
'''
def to_prefix_notation(expression, index):
    variables_set = set()
    expression = expression.replace('**', '^')

    summands = expression.split(' + ')
    prefix_expression = '(+'
    for summand in summands:
        multipliers = summand.split('*')
        prefix_multipliers = '(*'
        for multiplier in multipliers:
            if multiplier.isnumeric():
                prefix_multipliers = prefix_multipliers + ' ' + multiplier
            elif multiplier.isalpha():
                variable = multiplier + index
                variables_set.add(variable)
                prefix_multipliers = prefix_multipliers + ' ' + variable
            else:
                power = multiplier.split('^')
                variable = power[0] + index
                variables_set.add(variable)
                prefix_power = ' (^ ' + variable + ' ' + power[1] + ')'
                prefix_multipliers += prefix_power
        prefix_expression = prefix_expression + ' ' + prefix_multipliers + ')'
    prefix_expression += ')'
    return prefix_expression, variables_set


'''
def strInterp(i):
    s1=str(i)
    s="a"+s1+"*x+"+"b"+s1
    return s
'''

strings = []
strdiv = []
start = []
end = []
alf = ""
a = []
b = []
i1 = 0
div = 0
strings.append(str(input()))
while (strings[div] != ""):
    strings[div] = strings[div].replace(" ", "")
    string = strings[div]
    f = 0
    start = []
    end = []
    for i in range(len(string)):
        if string[i] == '-' or string[i] == '>':
            f = 1
        elif alf.find(string[i]) == -1:
            if f == 0:
                start.append(len(alf))
            else:
                end.append(len(alf))
            alf = alf + string[i]
        else:
            if f == 0:
                start.append(alf.find(string[i]))
            else:
                end.append(alf.find(string[i]))

    ls = len(start)
    le = len(end)
    d1 = i1
    a.append(" a" + str(start[0]))
    a.append("b" + str(start[ls - 1]))
    mul = ""
    br = ""

    # here we make strings

    startString = " + " + a[i1 + 1]
    startString1 = ""
    for i in range(ls - 1, 0, -1):
        mul = "(* a" + str(start[i]) + mul
        startString1 = "a" + str(start[i]) + "*" + startString1
        startString = " + " + startString1 + "b" + str(start[i - 1]) + startString
        br = ")" * (ls - i)
        a[i1 + 1] = "(+ " + mul + " b" + str(start[i - 1]) + br + " " + a[i1 + 1] + ")"
    startString = startString1 + "a" + str(start[0]) + "*x" + startString
    a[i1] = mul + a[i1] + br

    i1 = d1
    b.append(" a" + str(end[0]))
    b.append("b" + str(end[le - 1]))
    mul = ""
    br = ""

    endString = " + " + b[i1 + 1]
    endString1 = ""
    for i in range(le - 1, 0, -1):
        mul = "(* a" + str(end[i]) + mul
        endString1 = "a" + str(end[i]) + "*" + endString1
        endString = " + " + endString1 + "b" + str(end[i - 1]) + endString
        br = ")" * (le - i)
        b[i1 + 1] = "(+ " + mul + " b" + str(end[i - 1]) + br + " " + b[i1 + 1] + ")"
    endString = endString1 + "a" + str(end[0]) + "*x" + endString
    b[i1] = mul + b[i1] + br

    i1 += 2
    strdiv.append(i1)
    div += 1

    strings.append(str(input()))
    print(startString)
    print(endString)

# here we start working
with open('lab1.txt', 'w') as f:
    for i in range(len(alf)):
        f.write("(declare-fun a" + str(i) + " () Int)\n")
        f.write("(declare-fun b" + str(i) + " () Int)\n")
        # f.write("(declare-fun c"+str(i)+" () Int)\n")
        # f.write("(declare-fun d"+str(i)+" () Int)\n")
    for i in range(len(alf)):
        f.write("(assert (>= a" + str(i) + " 0))\n")
        f.write("(assert (>= b" + str(i) + " 0))\n")
        # f.write("(assert (> c"+str(i)+" 0))\n")
        # f.write("(assert (>= d"+str(i)+" 0))\n")

    n1 = 0
    for div1 in range(div):
        mainString = "(assert (or (and "
        xs1 = ""
        xs2 = ""
        nxs1 = ""
        nxs2 = ""
        if div1 > 0:
            n = (strdiv[div1] - strdiv[div1 - 1]) // 2 - 1
        else:
            n = strdiv[div1] // 2 - 1
        n2 = n1 + n
        s2 = ""
        for i in range(n1, n2 + 1):
            # print(i,n1,n2)
            s1 = "(> " + a[i] + " " + b[i] + ")"
            s2 = "(>= " + a[i] + " " + b[i] + ")"
            if i == n2:
                xs1 = xs1 + s1
                xs2 = xs2 + s2
            else:
                xs1 = xs1 + "(or " + s1 + " (and " + s2 + " "
                xs2 = xs2 + "(and " + s2 + " "
            s1 = "(> " + a[i + n + 1] + " " + b[i + n + 1] + ")"
            s2 = "(>= " + a[i + n + 1] + " " + b[i + n + 1] + ")"
            if i == n2:
                nxs1 = nxs1 + s1
                nxs2 = nxs2 + s2
            else:
                nxs1 = nxs1 + "(or " + s1 + " (and " + s2 + " "
                nxs2 = nxs2 + "(and " + s2 + " "

        for i in range(n):
            xs1 = xs1 + "))"
            xs2 = xs2 + ")"
            nxs1 = nxs1 + "))"
            nxs2 = nxs2 + ")"

        mainString = mainString + xs1 + " " + nxs2 + ") (and " + xs2 + " " + nxs1 + ")))\n"
        f.write(mainString)
        n1 = strdiv[div1]

    f.write("(check-sat)\n")
    f.write("(get-model)")

with open('lab1.txt', 'r') as f:
    smt_code = f.read()
solver = Solver()
solver.add(parse_smt2_string(smt_code))
result = solver.check()

if result == sat:
    print("Сounterexample")
    model = solver.model()
    for decl in model:
        print("%s = %s" % (decl, model[decl]))
elif result == unsat:
    print("Verification success\nThere will be DEMO\n")
else:
    print("Unknown")

expression = input("Enter expression: ")
simplified_expression = simplify_expression(expression)
print("Simplified expression:", simplified_expression)

prefix_expression, variables_set = to_prefix_notation(simplified_expression, '0')
print("Prefix notation:", prefix_expression)
print("Set of variables: ", variables_set)

'''
anotherstartString="x"
anotherendString="x"
for i in start:
    anotherstartString=anotherstartString.replace("x", "("+strInterp(i)+")")
for i in end:
    anotherendString=anotherendString.replace("x", "("+strInterp(i)+")")
'''

