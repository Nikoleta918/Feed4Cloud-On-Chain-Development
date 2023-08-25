# Required Libraries
import numpy as np

# Fuzzy AHP
from pyDecision.algorithm import fuzzy_ahp_method


def Fuzzy_Reputation(decision_matrix):
    fuzzy_weights, defuzzified_weights, normalized_weights, rc = fuzzy_ahp_method(decision_matrix)

    # #--uncomment to enable logs--
    # # Fuzzy Weigths (w)
    # print('Fuzzy Weigths')
    # for i in range(0, len(fuzzy_weights)):
    #     print('g' + str(i + 1) + ': ', np.around(fuzzy_weights[i], 3))
    #
    # print('Relative non-fuzzy Weigths (M)')
    # # Relative non-fuzzy Weigths (M) (per criterion)
    # for i in range(0, len(defuzzified_weights)):
    #     print('g' + str(i + 1) + ': ', round(defuzzified_weights[i], 3))
    #
    # print('Normalized Weigths (N)')
    # # Normalized Weigths (N) (per criterion)
    # for i in range(0, len(normalized_weights)):
    #     print('g' + str(i + 1) + ': ', round(normalized_weights[i], 3))

    return normalized_weights

def Update_Reputation(normalized_weights, predefined_weights, credibility, reputation_score):
    comparison_vector = normalized_weights.dot(predefined_weights)

    rating = comparison_vector[0][0]/comparison_vector[1][0]
    rating = credibility*rating*100


    w = 0.2
    print('Service reputation score before update', reputation_score)
    reputation_score = w*reputation_score + (1-w)*rating
    if  reputation_score < 0:
        reputation_score = 0
    elif  reputation_score > 5:
        reputation_score = 5

    print('Service reputation score after update', reputation_score)
    return reputation_score