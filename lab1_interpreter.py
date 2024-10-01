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

#Пока что временно ввод всего чего хотим вручную

#trs_variables=["x","y"]
trs_variables = str(input("variables = ")).split(',')
#trs_rules=["f(x)=a", "g(x)=f(f(x))", "u(x,y)=c(g(x),f(y))"]
trs_rules=[]
rules= input("input trs rules\n")
while rules!= "":
    trs_rules.append(rules)
    rules=input()
#grammar_rules=["a=1", "f(x)=x**2+2*x+1", "g(x)=x**3", "u(x,y)=x*y", "c(x,y)=x+y"]
grammar_rules=[]
rules= input("input grammar rules\n")
while rules!= "":
    grammar_rules.append(rules)
    rules=input()
constructors=[]
for i in range(len(grammar_rules)):
    constructors.append(grammar_rules[i][0])

#Я забыла как это действие с залезанием в скобки называется по нормальному, поэтому пока   будет называться podmena
#Потом заменю
def podmena(string):
    
    i=0
    if not (string[i] in constructors):
        return trs_variables[trs_variables.index(string[i])]
    con=constructors.index(string[i])
    
    if grammar_rules[con][1]=='=':
        return grammar_rules[con][2:]
    n=grammar_rules[con].count(',')+1
    rule=grammar_rules[con][2*n+3:]
    i=2
    s=""
    k=0 
    while k!=n and i<len(string):
        if string[i]==',':
            rule=rule.replace(grammar_rules[con][2*k+2],"("+podmena(s)+")")
            k+=1
            s=""
            i+=1
        s+=string[i]
        i+=1
    s=s[:-1]
    rule=rule.replace(grammar_rules[con][2*k+2],"("+podmena(s)+")")
    return rule



#-----------------------------------------------------------------------------
start_expressions=[]
end_expressions=[]
with open('lab1.txt', 'w') as f:
    for cr in range(len(trs_rules)):
        trs_rules[cr] = trs_rules[cr].replace(" ", "")
        
        start = trs_rules[cr][:(trs_rules[cr].find('='))]
        end = trs_rules[cr][(trs_rules[cr].find('=')+1):]
        
        start=simplify_expression(podmena(start))
        end=simplify_expression(podmena(end))
        
        
        start_expression, start_variables_set = to_prefix_notation(start, str(cr))
        end_expression, end_variables_set = to_prefix_notation(end, str(cr))
        variables_set=start_variables_set|end_variables_set
        start_expressions.append(start_expression)
        end_expressions.append(end_expression)
        for v in variables_set:
            f.write("(declare-fun " + v + " () Int)\n")
        #for v in variables_set:
        #    f.write("(assert (>= " + v + " 0))\n")
    for cr in range(len(trs_rules)): 
        f.write("(assert (<= " + start_expressions[cr] + " " + end_expressions[cr] + "))\n")
    f.write("(check-sat)\n")
    f.write("(get-model)")


''''
expression = input("Enter expression: ")
simplified_expression = simplify_expression(expression)
print("Simplified expression:", simplified_expression)

prefix_expression, variables_set = to_prefix_notation(simplified_expression, '0')
print("Prefix notation:", prefix_expression)
print("Set of variables: ", variables_set)
'''

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



