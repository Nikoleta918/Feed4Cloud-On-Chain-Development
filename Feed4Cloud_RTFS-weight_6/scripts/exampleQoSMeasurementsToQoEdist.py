# -*- coding: utf-8 -*-
"""
An example is provided which uses the scripts to approximate the QoE distribution 
in a system based on QoS measurements and an existing MOS mapping function. 

This tool is published under the license CC BY-SA 4.0 at
https://github.com/hossfeld/approx-qoe-distribution 

The following paper is to be cited in the bibliography whenever the tool is used.
[QoEMAN2020]
    Tobias Hossfeld, Poul E. Heegaard, Martin Varela, Lea Skorin-Kapov, Markus Fiedler. 
    "From QoS Distributions to QoE Distributions: a System's Perspective". 
    4th International Workshop on Quality of Experience Management (QoE Management 2020), 
    featured by IEEE Conference on Network Softwarization (IEEE NetSoft 2020), Ghent, Belgium.

Created on Thu Mar 26 21:51:00 2020
@author: Tobias Hossfeld
"""

import matplotlib.pyplot as plt
import numpy as np
import approxQoEdist as approx
import pandas as pd
import arff
from scipy.optimize import curve_fit


def QoS_to_QoE_mapping(qos_metric, qos):

    # %% Literature provides a MOS mapping function f
    # IQX hypothesis (a=4 reflects 5-point rating scale)
    # IQX hypothesis correlates QoE to QoS impairments such as packet loss or network delay
    # b=0.25 applicable in case of PLT according to "Fundamental Relationships for Deriving QoE in Systems"
    if qos_metric == 'PLT':
        a = 0.25
    elif qos_metric == 'Latency':
        a = 0.25

    f = lambda x: 4 * np.exp(-a * x) + 1
    # ITU-T recommending logarithmic correlation
    # to correlate QoE to the perceivable QoS resources such as bandwidth or bit rate
    # f = lambda x: a*np.log(x) + c
    plt.figure(10)
    plt.clf()

    # X denoting QoS distribution
    # x = np.linspace(0, 10, 100) #random QoS distribution
    x = qos  # actual distribution of QoS as reported in WebMOS dataset
    plt.plot(x, f(x))
    plt.xlabel(qos_metric)
    plt.ylabel('MOS')
    plt.grid(which='major')

    # %% Derive QoE distribution in the system using a discrete 5-point scale
    xk = np.arange(1, 6)  # The (discrete) QoE ratings (1,2,3,4,5)
    pk = np.zeros(5)  # Probability for QoE rating in the system
    for mos in f(qos):
        xkmos, pkmos = approx.getDiscreteDistributionArrays(mos)
        pk += pkmos
    pk /= len(qos)

    # %% Plot the QoE distribution and relevant QoE metrics
    plt.figure(11)
    plt.clf()
    plt.bar(xk, pk.cumsum(), label='system QoE')
    plt.xlabel('QoE rating')
    plt.ylabel('CDF')

    # %%  Those QoE metrics can also be derived using the fundamental relationships paper
    # Hoßfeld, T., Heegaard, P. E., Skorin-Kapov, L., & Varela, M. (2019, June).
    # Fundamental Relationships for Deriving QoE in Systems.
    # In 2019 Eleventh Int. Conf. on Quality of Multimedia Experience (QoMEX) (pp. 1-6). IEEE.

    mos_vals = f(qos)
    # print(f'Expected system QoE: E[Q]={(pk * xk).sum():.2f} vs. E[f(qos)]={mos_vals.mean():.2f}')
    plt.plot([mos_vals.mean()] * 2, [0, 1], 'k--', label=f'MOS={mos_vals.mean():.2f}')
    plt.text(mos_vals.mean(), 1, 'MOS')
    plt.gca().tick_params(right=True, top=True, labeltop=True)

    pow_vals = np.array([approx.getPoW(mos) for mos in f(qos)])
    # print(f'Poor or worse ratio in the system: PoW[Q]={pk[:2].sum():.2f} vs. E[w(qos)]={pow_vals.mean():.2f}')
    plt.plot([0.5, 5.5], [pow_vals.mean()] * 2, 'r--', label=f'PoW={pow_vals.mean():.2f}')
    plt.fill_between([0.5, 5.5], 0, [pow_vals.mean()] * 2, color='r', alpha=0.5, zorder=-1, hatch='--')

    gob_vals = np.array([approx.getGoB(mos) for mos in f(qos)])
    # print(f'Good or better ratio in the system: GoB[Q]={pk[-2:].sum():.2f} vs. E[g(qos)]={gob_vals.mean():.2f}')
    plt.plot([0.5, 5.5], [1 - gob_vals.mean()] * 2, 'g--', label=f'GoB={gob_vals.mean():.2f}')
    plt.fill_between([0.5, 5.5], [1 - gob_vals.mean()] * 2, 1, color='g', alpha=0.5, zorder=-1, hatch='--')

    plt.legend()
    # plt.show()

    print(f'Expected system QoE: E[f(qos)]={mos_vals.mean():.2f}')

    output_data = {
         'E[Q]': (pk * xk).sum(),
         'E[f(qos)]': mos_vals.mean(),
         'PoW[Q]': pk[:2].sum(),
         'GoB[Q]': pk[-2:].sum()
    }


    return output_data
