# Online Python - IDE, Editor, Compiler, Interpreter
import re
from sympy import simplify as sympy_simplify, expand, Symbol
from random import randint
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
''''
#trs_rules=[
f(x)=a
g(x)=f(f(x))
u(x,y)=c(g(x),f(y))
"]'
'''
trs_rules=[]
rules= input("input trs rules\n")
while rules!= "":
    trs_rules.append(rules)
    rules=input()
''''
#grammar_rules=["
a=1
f(x)=x**2+2*x+1
g(x)=x**3
u(x,y)=x*y
c(x,y)=x+y
"]
'''
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
    c=1
    while k!=n and i<len(string):
        if string[i]==',' and c==1:
            rule=rule.replace(grammar_rules[con][2*k+2],"("+podmena(s)+")")
            k+=1
            s=""
            i+=1
        elif string[i]==')':
            c-=1
        elif string[i]=='(':
            c+=1
        s+=string[i]
        i+=1
    s=s[:-1]
    rule=rule.replace(grammar_rules[con][2*k+2],"("+podmena(s)+")")
    return rule

def random_line(k,n,terms,l):
    t=randint(0,k)
    if l==1:
        s=terms[t][0]+'('
        for i in range(n[t]):
            s=s+trs_variables[0]+'0,'
        s=s[:-1]+')'
        return s
    s=terms[t][0]+'('
    for i in range(n[t]):
        s=s+random_line(k,n,terms,l-1)+','
    s=s[:-1]+')'
    return s
    
    
def demo():
    k=0
    n=[]
    terms=[]
    for s in grammar_rules:
        if s[1]=='(':
            k+=1 
            n.append(s.count(',')+1)
            terms.append(s)
    l=randint(1,10)
    s1=random_line(k-1,n,terms,l)
    li=randint(1,5)
    s2=s1
    for i in range (li):
        for j in trs_rules:
            if s2.find(j[0])!=-1:
                a=s2.find(j[0])+2
                b=0
                for rule in range(k):
                    if terms[rule][0]==j[0]:
                        b=rule
                        break
                var_n=n[b]
                new_s=j[j.find('=')+1:]
                sub_s=""
                c=1
                t=0
                i=0
                while t==0:
                    if s2[a]==',':
                        if c==1:
                            new_s=new_s.replace(terms[b][2*i+2],sub_s)
                            sub_s=""
                            i+=1
                        else:
                            sub_s=sub_s+s2[a]
                    elif s2[a]==')':
                        if c==1:
                            new_s=new_s.replace(terms[b][2*i+2],sub_s)
                            sub_s=""
                            t=1
                        else:
                            sub_s=sub_s+s2[a]
                            c+=1
                    elif s2[a]=='(':
                        sub_s=sub_s+s2[a]
                        c-=1
                    else:
                        sub_s=sub_s+s2[a]
                    a+=1
                s2=s2[:s2.find(j[0])]+new_s+s2[a:]
                break
    s1=s1.replace(trs_variables[0]+'0', trs_variables[0])
    s2=s2.replace(trs_variables[0]+'0', trs_variables[0])
    return s1,s2



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
''''
s1,s2 = demo()
print(s1)
print(s2)
s1=str(s1).replace(trs_variables[0], '1')
s2=str(s2).replace(trs_variables[0], '1')
s1=simplify_expression(s1)
s2=simplify_expression(s2)
print(s1)
print(s2)
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
    s1,s2 = demo()
    print(s1)
    print(s2)
    s1=simplify_expression(podmena(s1))
    s2=simplify_expression(podmena(s2))
    print(s1)
    print(s2)
    s1=str(s1).replace(trs_variables[0], '1')
    s2=str(s2).replace(trs_variables[0], '1')
    s1=simplify_expression(s1)
    s2=simplify_expression(s2)
    print(s1)
    print(s2)
else:
    print("Unknown")

