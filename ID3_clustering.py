import os
import math
import numpy as np

def calculate_probabilities(data):
    positive = 0
    total = 0

    probability_positive = 0
    probability_negative = 0

    for i in data:
        total = total + 1
        if i == True:
            positive = positive + 1
    
    probability_positive = positive/total
    probability_negative = 1-probability_positive

    return (probability_positive, probability_negative)


def calcuate_entropy_output(data_output, probability_output):
    entropy = -probability_output[1] * math.log2(probability_output[1]) - probability_output[0] * math.log2(probability_output[0])
    return entropy

def calcuate_entropy_input(data_input, data_output):
    indicies_positive = []
    indicies_negative = []
    count_positive = 0
    count_negative = 0
    entropy = []
    

    for i in range(len(data_input)):
        if data_input[i] == True:
            indicies_positive.append(i)
        elif data_input[i] == False:
            indicies_negative.append(i)

    for i in indicies_negative:
        if data_input[i] == data_output[i]:
            count_negative = count_negative + 1
    
    for i in indicies_positive:
        if data_input[i] == data_output[i]:
            count_positive = count_positive + 1
    
    if count_positive == len(indicies_positive) or count_positive == 0:
        entropy.append(0)
    else:
        probability = count_positive/len(indicies_positive)
        entropy.append((-probability * math.log2(probability)) - ((1-probability) * math.log2(1-probability)))
    
    if count_negative == len(indicies_negative) or count_negative == 0:
        entropy.append(0)
    else:
        probability = count_negative/len(indicies_negative)
        entropy.append((-probability * math.log2(probability)) - ((1-probability) * math.log2(1-probability)))

    return entropy

def calculate_sum_of_entropies(probabilities, entropy_input):
    sum_of_entropies = probabilities[0] * entropy_input[0] + probabilities[1] * entropy_input[1]
    return(sum_of_entropies)

def give_interpretation(information_gain, keys):
    num_attributes = len(information_gain)
    infomation_gain_sorted = sorted(information_gain, reverse=True)
    count = 0
    while count < (num_attributes-1):
        information_gain_index = information_gain.index(infomation_gain_sorted[count])
        print(f"""
            Node {count+1}: {keys[information_gain_index][0]} (information_gain: {information_gain[information_gain_index]})
                    {keys[information_gain_index][1]} = {keys[num_attributes][1]} {keys[num_attributes][0]}
                    {keys[information_gain_index][2]} = go to node {count+2}
        """)
        count = count + 1
    information_gain_index = information_gain.index(infomation_gain_sorted[count])
    print(f"""
            Node {count+1}: {keys[information_gain_index][0]} (information_gain: {information_gain[information_gain_index]})
                    {keys[information_gain_index][1]} = {keys[num_attributes][1]} {keys[num_attributes][0]}
                    {keys[information_gain_index][2]} = {keys[num_attributes][2]} {keys[num_attributes][0]}
    """)
        
def main():
    #insert data labels only as a list or tuple
    key = (("age", "< 25", "≥ 25"), ("income", "< $50,000", "> $50,000"), ("gender", "female", "male"), ("risk", "high", "low"))

    #insert data here as a n-D tuple, wherein the last inner tuple is the output
    data = ((True, True, False, False, False, True, True, True),(False, False, True, False, False, True, True, True),(False, True, True, True, False, False, False, True), (True, True, True, False, False, True, True, True))

    #gets information dynamically from the data
    data_size = len(data[0])
    data_dimension = len(data)

    #calculates probabilities
    probabilities = []
    entropy_input = []
    entropy_input_weighted = []
    information_gain = []
    
    for i in data:
        probabilities.append(calculate_probabilities(i))

    entropy_output = calcuate_entropy_output(data[data_dimension-1], probabilities[data_dimension-1])

    for i in range(data_dimension-1):
        entropy_input.append(calcuate_entropy_input(data[i], data[data_dimension-1]))
        entropy_input_weighted.append(calculate_sum_of_entropies(probabilities[i],entropy_input[i]))
        information_gain.append(entropy_output-entropy_input_weighted[i])

    give_interpretation(information_gain, key)

main()