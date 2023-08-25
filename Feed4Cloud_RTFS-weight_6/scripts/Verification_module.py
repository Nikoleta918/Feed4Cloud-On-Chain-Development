import numpy as np


def Verification(expected, actual):
    if abs(actual - expected) <= 1.75:
        print('Verification success')
        return True
    else:
        print('Verification failed')
        return False


def Fuzzy_Verification(expected, actual):
    distance = np.sqrt(
        ((expected[0] - actual[0]) ** 2 + (expected[1] - actual[1]) ** 2 + (expected[2] - actual[2]) ** 2) / 3)

    if distance < 5:
        print('Verification success')
        return True
    else:
        print('Verification failed')
        return False
