# Required Libraries
import numpy as np


def Credibility_rating(result, fakes):
    theta = 0.5
    a = 1
    if not result:
        return 5
    else:
        return -theta * np.exp(a * (1 - fakes))


def Update_credibility(credibility, result, fakes):
    w = 0.75

    rating = Credibility_rating(result, fakes)
    print('User credibility before update', credibility)
    credibility = w * credibility + (1 - w) * rating
    if credibility < 0:
        credibility = 0
    elif credibility > 5:
        credibility = 5
    print('User credibility after update', credibility)

    return credibility
