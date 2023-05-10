import math

def mutual_information(data, label):
    terms = []
    information = 0

    for i in range(len(data)):
        try:
            terms.append(data[i][0] * math.log2(data[i][0]/(data[i][1]*data[i][2])))
        except:
            terms.append(0)
    for i in range(len(terms)):
        information = information + terms[i]

    #return terms, information

    print(f'''
        ********
        {label}
            mutual information = {information}
          ''')

    #print(terms)
    #print(information)

def chi_squared(data, observations):
    terms = []
    cq_number = 0

    for i in range(len(data)):
        try:
            observed = data[i][3]
            expected_probability = data[i][1]* data[i][2]
            expected = expected_probability * observations

            top = observed-expected
            top_squared = top**2
            chi = top_squared/expected
        
            terms.append(chi)
        except:
            terms.append(0)

    for i in range(len(terms)):
        cq_number = cq_number + terms[i]

    #print(terms)
    #print(cq_number)

    print(f'''
            chi squared = {cq_number}
        ********
          ''')


def main():
    labels = ('age','income','sex')
    observations = 8
    data = (((0.5,0.5,0.625,4), (0,0.5,0.375,0), (0.125,0.5,0.625,1), (0.375,0.5,0.375,3)), ((0.25,	0.625,	0.625,	2),(0.375,	0.375,	0.375,	3),(0.375,	0.625,	0.625,	3),(0,	0.375,	0.375,	0)), ((0.375,	0.5, 0.625,	3),(0.125,	0.5, 0.375,	1),(0.25, 0.5, 0.625, 2),(0.25,	0.5, 0.375,	2)))
    for i in range(len(data)):
        mutual_information(data[i], labels[i])
        chi_squared(data[i], observations)

main()


