#Author: Robert Hart
#Purpose: A Python program to perform the EM algorithm per HW3

import os
import sympy as sp
import pandas as pd

def calculate_liklihood_terms(instances):
    liklihood_terms = []
    for i in range(len(instances)):
        liklihood_terms.append(instances[i][2]**instances[i][1])
    return liklihood_terms


def create_liklihood_function(liklihood_terms):
    C = sp.Symbol('C', positive = True)
    P = C
    for i in liklihood_terms:
        P = P * i
    return P

def calculate_maximum_liklihood_equation(P, θ):
    P_log = sp.log(P)
    P_log_expand = sp.expand_log(P_log)
    P_derivative = P_log_expand.diff(θ)
    P_derivative_solution = sp.solve(P_derivative, θ)
    maximum_liklihood_equation = sp.nsimplify(P_derivative_solution[0])
    return maximum_liklihood_equation

def create_expectation_equation(instances, rules):
    expectation_expressions_symbols = []
    expectation_expressions_strings = []
    for rule in rules:
        rule_symbols = []
        instance_indicies = []
        probabilities = []

        for i in range(len(rule[1])):
            rule_symbols.append(sp.Symbol(rule[1][i], positive = True))

        #find rule symbols in data

        for symbol in rule_symbols:
            for j in range(len(instances)):
                for k in range(len(instances[j])):
                    if symbol == instances[j][k]:
                        instance_indicies.append(j)

        for instance_index in instance_indicies:
            probabilities.append(instances[instance_index][2])
        
        if rule[2] == "add":
            probability_total = 0
            for probability in probabilities:
                probability_total = probability_total + probability
            probabilities.append(probability_total)

        #can add other cases later with elif/else

        for i in range(len(rule[1])):
            expression_symbol = sp.nsimplify(probabilities[i]/probabilities[len(probabilities)-1] * sp.Symbol(rule[0]))
            expression_string = f'{rule_symbols[i]} = {expression_symbol}'
            expectation_expressions_symbols.append(expression_symbol)
            expectation_expressions_strings.append(expression_string)

    
    return expectation_expressions_symbols, expectation_expressions_strings


def find_best_expectation_expression(expectation_expressions_strings):
    theta_count = []
    for expression in expectation_expressions_strings:
        theta_count.append(expression.count("θ"))
    best_expression = theta_count.index((max(theta_count)))
    return best_expression
        

def EM_iteration(iterations, rules, MLE, symbols_class, current, expression, θ):

    theta = 0
    reference_key = -1


    current_instance = ""

    #dictionaries for symbol substitutions
    substiution_dict_MLE = {}
    substiution_dict_ee = {}

    for rule in rules:
        substiution_dict_MLE[rule[4]] = rule[3]
        substiution_dict_ee[rule[4]] = rule[3]
        

    for i in range(len(symbols_class)):
        substiution_dict_ee[symbols_class[i][0]] = symbols_class[i][1]
        substiution_dict_MLE[symbols_class[i][0]] = symbols_class[i][1]
        if i == current:
            reference_key = symbols_class[i][0]
            current_instance = symbols_class[i][1]

    MLE_list = []
    EE_list = []
    index_list = []
    space_list = []

    substiution_dict_ee[θ] = 0

    count = 1

    for i in range(iterations):
        #calculate ee with correct substitution dictionary
        expectation_expression = expression.subs(substiution_dict_ee).n()
        #update atribute for MLE
        substiution_dict_MLE[reference_key] = expectation_expression
        theta = MLE.subs(substiution_dict_MLE).n()
        substiution_dict_ee[θ] = theta
        EE_list.append(expectation_expression)
        MLE_list.append(theta)
        index_list.append(count)
        space_list.append("")
        count = count + 1

    data_dictionary = {'t': index_list,f'{reference_key}^t': EE_list , 'θ^t': MLE_list, 'SPACER': space_list} 
    data_dataframe = pd.DataFrame.from_dict(data_dictionary)

    return data_dataframe

def main():
    #defines theta
    θ = sp.Symbol('θ', positive = True)

    #insert data here
    instances = (("A", sp.Symbol('a',positive = True), 1/3), ("C", sp.Symbol('c',positive = True), θ), ("G", sp.Symbol('g',positive = True), 1/3), ("T", sp.Symbol('t',positive = True), 1/3-θ))

    seed = 10

    iterations = 10 #number of iterations to run EM
    rules = [["x","ac","add",20, sp.Symbol('x')],["y","gt","add",20, sp.Symbol('y')]]  #rule format is {variable},{variables making up expression},{operator}
    
    #dynamically creates data
    symbols_class = []
    for instance in instances:
        temp = []
        temp.append(instance[1])
        temp.append(seed)
        symbols_class.append(temp)


    liklihood_terms = calculate_liklihood_terms(instances)
    P = create_liklihood_function(liklihood_terms)
    MLE = calculate_maximum_liklihood_equation(P, θ)
    ee_symbols, ee_strings = create_expectation_equation(instances, rules)
    
    
    #output after finding MLE and expectation expressions
    print(f'\tLOG-LIKELIHOOD MLE EXPRESSION:\n\t\tθ = {MLE}\n')
    print(f'\n\tEXPECTATION EXPRESSIONS:')
    for expression in ee_strings:
        print(f'\t\t{expression}\n')

    dataframes = []

    #iterate every expectation exression for every base
    for current in range(len(ee_symbols)):
        dataframes.append(EM_iteration(iterations, rules, MLE, symbols_class, current, ee_symbols[current], θ))

    final_dataframe = pd.concat(dataframes, axis=1)

    final_dataframe.to_csv("em_algorithm_out.csv", index=False)

    print("\n\t!!!DATA SAVED TO CSV!!!")


main()
