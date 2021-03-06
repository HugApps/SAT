import random
import time
import copy

import sys

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
#####################################################
#####################################################


# A clause consists of a set of symbols, each of which is negated
# or not. A clause where
# clause.symbols = {"a": 1, "b": -1, "c": 1}
# corresponds to the statement: a OR (NOT b) OR c .
class Clause:
    def __init__(self):
        pass

    def from_str(self, s):
        s = s.split()
        self.symbols = {}
        for token in s:
            if token[0] == "-":
                sign = -1
                symbol = token[1:]
            else:
                sign = 1
                symbol = token
            self.symbols[symbol] = sign

    def __str__(self):
        tokens = []
        for symbol,sign in self.symbols.items():
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            tokens.append(token)
        return " ".join(tokens)

# A SAT instance consists of a set of CNF clauses. All clauses
# must be satisfied in order for the SAT instance to be satisfied.
class SatInstance:
    def __init__(self):
        pass

    def from_str(self, s):
        self.symbols = set()
        self.clauses = []
        for line in s.splitlines():
            clause = Clause()
            clause.from_str(line)
            self.clauses.append(clause)
            for symbol in clause.symbols:
                self.symbols.add(symbol)
        self.symbols = sorted(self.symbols)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s

    # Takes as input an assignment to symbols and returns True or
    # False depending on whether the instance is satisfied.
    # Input:
    # - assignment: Dictionary of the format {symbol: sign}, where sign
    #       is either 1 or -1.
    # Output: True or False
    def is_satisfied(self, assignment):
        ###########################################
        # Start your code
        if assignment.__len__() == False:
            return False
        else:
            for clause in self.clauses:
                print(clause)
            return True
        return False;
        # End your code
        ###########################################

# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: SAT instance
# Output: Dictionary of the format {symbol: sign}, where sign
#         is either 1 or -1.
def evalExpression(expression) :
    running_bool = expression[0]
    for i in range(1,expression.__len__()):
        running_bool = running_bool or expression[i]
    return running_bool

def getBool (val):
    if val < 0:
        return False
    else:
        return True

def back_track(assignment,sym):
    # this is called when the current assignment fails , we pop the latest assignment if its already false, otherwise set to true
    print("back track")
    if assignment[sym] == 1:
        assignment[sym] = -1;
    else:
        del assignment[sym]
    return

def solve_dpll(instance):
    ###########################################
    # Start your code
    # find the first sym and assign it a value
    assignment = {}
    #find_pure_symbol(instance,assignment)
    print(dpll(instance, assignment))
    print(assignment)
    return assignment


def has_empty_clause(instance):
    for clause in instance.clauses:
        if clause.symbols.__len__() == 0:
            return True
    return False


def dpll (instance,assignment):
   # print(assignment)
    print("-----------------------------")
    if instance.clauses.__len__() == 0:
        print("nothing to evalulate")
        return True , assignment
    if has_empty_clause(instance) == True:
        print("EMpty clause")
        return False ,assignment

    else:
        unit_clauses = find_unit_clause(instance,assignment)
        if unit_clauses.__len__() >= 1:
         return dpll(simpliyfy(copy.deepcopy(instance),int(unit_clauses[0]),copy.deepcopy(assignment)),copy.deepcopy(assignment))

        nextSymbol = instance.symbols.pop(0)
        print(nextSymbol)
        assignment[nextSymbol] = 1
        print(assignment)
        print("true assignment")
        if dpll(simpliyfy(copy.deepcopy(instance),nextSymbol,copy.deepcopy(assignment)),copy.deepcopy(assignment)) == True:
            return True,assignment
        else:
            print("false assignment")
            assignment[nextSymbol] = -1
            print(assignment)
            return dpll(simpliyfy(copy.deepcopy(instance),nextSymbol,copy.deepcopy(assignment)),copy.deepcopy(assignment))




# get symbol not already in assignment
def simpliyfy (instance,literal,assignment):
    to_delete = []
    assignedVal = assignment[str(literal)]
    print("remove instances of literal" +str(literal))
    for clause in instance.clauses:
        if str(literal) in clause.symbols.keys():
            if clause.symbols[str(literal)] == assignedVal:
               # print(clause)
                to_delete.append(clause)
            else:
                del clause.symbols[str(literal)]
    for clause in instance.clauses:
        if "remove" in clause.symbols.values():
            del clause.symbols[literal]
    for clauseToDelete in to_delete:
        instance.clauses.remove(clauseToDelete)
    return instance




    # End your code
    ###########################################
# find clause that only has a single literal, that has not been assigned, removes clauses that contain this unit clause
def find_unit_clause (instance,assignment):
    unit_clauses=[]
    for clause in instance.clauses:
        if clause.symbols.__len__() == 1:
             for key in clause.symbols:
                 assignment[key] = clause.symbols[key]
                 unit_clauses.append(key)
    return unit_clauses
# pure symbol only appear as a or -a exclusively?????????????????????????????????????????"'?
def find_pure_symbol (instance,model):
   stackOfSym = []
   for sym in instance.symbols:
     for clause in instance.clauses:
         if sym in clause.symbols:
             # INTIAL STACK IS EMPTY, ASSIGN FIRST VALUE OF FIRST CLAUSE INCLUDING THE SYMBOL
             if stackOfSym.__len__() ==0 :
                 value = clause.symbols[sym]
                 stackOfSym.append((sym,value))
             else:
                 valueNew = clause.symbols[sym]
                 valueOld = stackOfSym[0][1]
                 if valueOld != valueNew:
                    stackOfSym=[]

     if stackOfSym.__len__() == 1:
         return stackOfSym
            #if clause.symbols[0] senot in model:


with open("test_assign.txt", "r") as input_file:
    instance_strs = input_file.read()

instance_strs = instance_strs.split("\n\n")


with open("small_assignments_inferred.txt", "w") as output_file:
    for instance_str in instance_strs:
        if instance_str.strip() == "":
            continue
        instance = SatInstance()
        instance.from_str(instance_str)
        assignment = solve_dpll(instance)
        print(assignment)
        for symbol_index, (symbol,sign) in enumerate(assignment.items()):
            if symbol_index != 0:
                output_file.write(" ")
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            output_file.write(token)
        output_file.write("\n")
















