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

        for clause in self.clauses:

            if set(assignment.keys()) == set(clause.symbols.keys()):
                # Build expression
                expression = []
                for key in clause.symbols:
                    currentVal = getBool(assignment[key])
                    if getBool(clause.symbols[key]) == False:
                        expression.append( not currentVal)
                    else:
                        expression.append(currentVal)
                # evalulate expression

                if evalExpression(expression) == False :

                    return False

        return True;
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
    count = 0
    currentVar = instance.symbols[0]
    assignVar(assignment,currentVar)
    while assignment.__len__() > 0 :

        if instance.is_satisfied(assignment) == True and assignment.__len__() == instance.symbols.__len__():
            return assignment
        if instance.is_satisfied(assignment) == False:
            if assignment[currentVar] == -1:
                del assignment[currentVar]
                count = count -1
                currentVar = instance.symbols[count]
                assignVar(assignment, currentVar)
            else:
                count = count
                currentVar = instance.symbols[count]
                assignment[currentVar] = -1

        else:
            count = count + 1
            currentVar = instance.symbols[count]
            assignVar(assignment,currentVar)





def assignVar (assignment,val):
    if val not in assignment:
        assignment[val] = 1
    else:
        assignment[val] = -1


    # End your code
    ###########################################

with open("small_instances.txt", "r") as input_file:
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
















