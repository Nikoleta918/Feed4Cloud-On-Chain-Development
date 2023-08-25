from flask import Flask
from flask_restful import Resource, Api

import requests
from web3 import Web3
import json

from eth_account import Account


import pandas as pd
import arff
import numpy as np


import QoSQoEmapper as QoE_map
import Verification_module
import Reputation_model
import Credibility_mechanism
import RTFS_repo

#from metric_collector import MetricCollector
import os

import time
import pytz


app = Flask(__name__)
app.config["BUNDLE_ERRORS"] = True
api = Api(app)

monitoring_port = int(os.getenv("MONITORING_PORT", 8000))
metric_prefix = "netdata:" + os.getenv("PREFIX", "c9yiksjxsn:t653zqdtp4:tjy2jkfwpn")
#collector = MetricCollector(monitoring_port, metric_prefix)

local_tz = pytz.timezone('Europe/Athens')


def RTFS():

    ### Input data: Monitoring data and user feedback #####

    version = 1

    if version == 1:

        # v1: Real-time data
        print("Getting real-time QoS measurements..")
        qos_data = {}

        prometheus = 'https://maestro-prometheus.ubitech.eu/'
        prometheus_instance = 'netdata:c9yiksjxsn:t653zqdtp4:tsrswvxk8y'
        start_time = int(time.time() - 16 * 60)  # to get data for past 15 minutes
        end_time = int(time.time() - 0.5 * 60)
        response = requests.get(prometheus + '/api/v1/query_range',
                                params={'query': prometheus_instance + '_net_net_kilobits_persec_average', 'start': start_time,
                                        'end': end_time, 'step': '30s'})
        # print(response.json())
        prometheus_data = response.json()

        data_list = []
        for i in prometheus_data['data']['result']:
            if i['metric']['dimension'] == 'received' and i['metric']['family'] == 'ens3':  # this is used for 'netdata_net_net_kilobits_persec_average' metric
                for val in i['values']:
                    timestamp = val[0]
                    value = float(val[1])
                    data_list.append([timestamp, value])

        df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')

        qos_data['Latency'] = df['value']
        # print(qos_data)
        # exit()
        #
        # response = requests.get(prometheus + '/api/v1/query_range',
        #                         params={'query': prometheus_instance + 'net_packets_packets_persec_average', 'start': start_time,
        #                                 'end': end_time, 'step': '30s'})
        # print(response.json())
        # prometheus_data = response.json()
        #
        # data_list = []
        # for i in prometheus_data['data']['result']:
        #     if i['metric']['dimension'] == 'received' and i['metric']['family'] == 'ens3':
        #         for val in i['values']:
        #             timestamp = val[0]
        #             value = float(val[1])
        #             data_list.append([timestamp, value])
        #
        # df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
        # df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        # df = df.set_index('timestamp')
        #
        # qos_data['Received packets'] = df['value']
        # print(qos_data)
        # exit()

        response = requests.get(prometheus + '/api/v1/query_range',
                                params={'query': prometheus_instance + '_net_drops_drops_persec_average', 'start': start_time,
                                        'end': end_time, 'step': '30s'})
        # print(response.json())
        prometheus_data = response.json()

        data_list = []
        for i in prometheus_data['data']['result']:
            if i['metric']['dimension'] == 'inbound' and i['metric']['family'] == 'ens3':
                for val in i['values']:
                    timestamp = val[0]
                    value = float(val[1])
                    data_list.append([timestamp, value])

        df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')

        qos_data['Packet Drops'] = df['value']
        # print(qos_data)
        # exit()

        response = requests.get(prometheus + '/api/v1/query_range',
                                params={'query': prometheus_instance + '_net_errors_errors_persec_average', 'start': start_time,
                                        'end': end_time, 'step': '30s'})
        # print(response.json())
        prometheus_data = response.json()

        data_list = []
        for i in prometheus_data['data']['result']:
            if i['metric']['dimension'] == 'inbound' and i['metric']['family'] == 'ens3':
                for val in i['values']:
                    timestamp = val[0]
                    value = float(val[1])
                    data_list.append([timestamp, value])

        df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')

        qos_data['Errors'] = df['value']
        # print(qos_data)
        # exit()

        response = requests.get(prometheus + '/api/v1/query_range',
                                params={'query': prometheus_instance + '_system_idlejitter_microseconds_lost_persec_average', 'start': start_time,
                                        'end': end_time, 'step': '30s'})
        # print(response.json())
        prometheus_data = response.json()

        data_list = []
        for i in prometheus_data['data']['result']:
            if i['metric']['dimension'] == 'average':
                for val in i['values']:
                    timestamp = val[0]
                    value = float(val[1])
                    data_list.append([timestamp, value])

        df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')

        qos_data['Idle jitter'] = df['value']
        # print(qos_data)

        response = requests.get(prometheus + '/api/v1/query_range',
                                params={'query': prometheus_instance + '_system_uptime_seconds_average', 'start': start_time,
                                        'end': end_time, 'step': '30s'})
        # print(response.json())
        prometheus_data = response.json()

        data_list = []
        for i in prometheus_data['data']['result']:
            for val in i['values']:
                timestamp = val[0]
                value = float(val[1])
                data_list.append([timestamp, value])

        df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')

        qos_data['Uptime'] = df['value']
        # print(qos_data)

        response = requests.get(prometheus + '/api/v1/query_range',
                                params={'query': prometheus_instance + '_cpu_cpu_percentage_average', 'start': start_time,
                                        'end': end_time, 'step': '30s'})
        # print(response.json())
        prometheus_data = response.json()

        data_list = []
        for i in prometheus_data['data']['result']:
            if i['metric']['dimension'] == 'idle':
                for val in i['values']:
                    timestamp = val[0]
                    value = 100 - float(val[1])
                    data_list.append([timestamp, value])


        df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')

        qos_data['CPU'] = df['value']
        print(qos_data)
        # exit()

        # save qos_data to CSV file
        df = pd.DataFrame.from_dict(qos_data, orient='index').transpose()

        df.index = df.index.tz_localize(pytz.utc)
        df.index = df.index.tz_convert('Europe/Athens')

        #Avoid duplicates
        try:
            csv_qos_data = pd.read_csv('qos_data.csv', index_col='timestamp')

            csv_qos_data.index = pd.to_datetime(csv_qos_data.index)
            df = df.loc[df.index > csv_qos_data.index[-1]]
        except FileNotFoundError:
            pass

        with open('qos_data.csv', mode='a') as f:
            df.to_csv(f, header=f.tell() == 0, index_label='timestamp')

        ##Getting ratings from Blockchain client
        print("Retrieving user ratings from Blockchain..")

        # when deployed on Ganache for local testing
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

        with open(
                 'C:\\Users\\super\\Desktop\\feed4cloudProjects\\feed4cloud_weight_6\\feed4Cloud.json') as json_file:
             abi = json.load(json_file)
        contract_address = '0x4c5fdd1fc61929D7F3f9C798e6B8F3f531e57377'


        # when deployed on Alastria Red-B network
        # w3 = Web3(Web3.HTTPProvider('http://54.195.253.191:8545'))
        #path = None
        #if (os.name == "nt"):
        #    path = 'C:\\Users\\super\\Desktop\\Feed4Cloud_RTFS-main\\ALASTRIA_API_KEY.txt'
        #else:
        #    path = os.getenv("ALASTRIA_KEY_PATH")

        #with open(path, 'r') as api_key_file:
        #    key = api_key_file.read().strip()  # when deployed on Alastria Red-B
       # provider = 'https://red-b.alastria.io/v0/' + key

       # w3 = Web3(Web3.HTTPProvider(provider))

        # with open(
        #         'C:\\Users\\Iwanna\\Desktop\\Ph.D\\Work\\Proposals\\Projects\\Feed4Cloud\\Implementation\\ABI_alastria.json') as json_file:
       # path = None
       # if (os.name == "nt"):
       #     path = 'C:\\Users\\super\\Desktop\\Feed4Cloud_RTFS-main\\ABI_alastria.json'
      #  else:
       #     path = os.getenv("ALASTRIA_OBJ_PATH")


        #with open(path) as json_file:
        #            abi = json.load(json_file)  # when deployed on Alastria Red-B

        #contract_address = '0xE14688a3fe21D25838b6F6E2d2951C3e391726A6'
        contract = w3.eth.contract(address=contract_address, abi=abi)
        service_id = 74178
        recorded_ratings = contract.functions.getServiceRatings(service_id).call()
        ratings = []

        for rating in recorded_ratings:
            ratings.append({'serviceId': rating[0], 'userId': rating[1], 'rating': rating[2],
                            'timestamp': pd.to_datetime(rating[3], unit='s')})

        print(ratings)
        # exit()

        service_id = '74178'
        service = RTFS_repo.Service(service_id) # Feed4Cloud service

        weight_matrix = np.array([[0.2], [0.1], [0.1], [0.2], [0.2], [0.2]])

    elif version == 2:
        # v2: Dataset
        dataset = arff.load(
            open(r'C:\Users\Iwanna\Desktop\Ph.D\Work\Proposals\Projects\Feed4Cloud\Implementation\webmos-9k-sanitized.arff',
                 'r'))

        columns = [i[0] for i in dataset['attributes']]
        data = pd.DataFrame(dataset['data'], columns=columns)

        # # %% QoS measurements in the system
        # k = len(data)

        # qos = np.abs(np.random.randn(k) * 2 + 8.6)  # here randomly generated values
        qos_data = {'PLT': data['onload'], 'Latency': data[
            'latency']}  # qos values as reported in WebMOS dataset (https://webqoe.telecom-paristech.fr/data/)

        weight_matrix = np.array([[0.5], [0.5]])
        service = RTFS_repo.Service(0)
        service_user = RTFS_repo.User(0)

    latest_qos_timestamp = pd.Timestamp('2023-02-28 00:00:00')

    QoE_metrics = [{}] * len(qos_data.keys())

    for metric, i in zip(qos_data.keys(), range(len(qos_data.keys()))):
        if qos_data[metric].index.max() > latest_qos_timestamp:
            latest_qos_timestamp = qos_data[metric].index.max()
        # Calling QoS-to-QoE mapper
        QoE_metrics[i] = QoE_map.QoS_to_QoE_mapping(metric, qos_data[metric])


    print("Checking if there are any recent user ratings for Feed4Cloud service to be verified..")

    for rating in ratings:
        mismatches = 0

        if rating['timestamp'] < latest_qos_timestamp:
            continue

        if version == 1:
            qoe_data = {'timestamp': [rating['timestamp']], 'Actual rating': [rating['rating']]}

            if rating['rating'] == 1.0:  # Very Poor (VP)
                fuzzy_rating = (1, 1, 3)
            elif rating['rating'] == 2.0:  # Poor (P)
                fuzzy_rating = (1, 3, 5)
            elif rating['rating'] == 3.0:  # Medium (M)
                fuzzy_rating = (3, 5, 7)
            elif rating['rating'] == 4.0:  # Good (G)
                fuzzy_rating = (5, 7, 9)
            elif rating['rating'] == 5.0:  # Very Good (VG)
                fuzzy_rating = (7, 9, 9)
            #apla vale to service_user kai valto kapws credibility kapws san parametro
            service_user = RTFS_repo.User(rating['userId'])

            norm_weight_matrix = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])

        else:

            if rating == 1.0:  # Very Poor (VP)
                fuzzy_rating = (1, 1, 3)
            elif rating == 2.0:  # Poor (P)
                fuzzy_rating = (1, 3, 5)
            elif rating == 3.0:  # Medium (M)
                fuzzy_rating = (3, 5, 7)
            elif rating == 4.0:  # Good (G)
                fuzzy_rating = (5, 7, 9)
            elif rating == 5.0:  # Very Good (VG)
                fuzzy_rating = (7, 9, 9)

            norm_weight_matrix = np.array([[0.0, 0.0], [1.0, 1.0]])


        for metric, i in zip(qos_data.keys(), range(len(qos_data.keys()))):

            # save expected qoe to CSV file
            qoe_data[metric] = [QoE_metrics[i]['E[f(qos)]']]


            if QoE_metrics[i]['E[f(qos)]'] < 1.5:  # Very Poor (VP)
                fuzzy_qoe = (1, 1, 3)
            elif QoE_metrics[i]['E[f(qos)]'] < 2.5:  # Poor (P)
                fuzzy_qoe = (1, 3, 5)
            elif QoE_metrics[i]['E[f(qos)]'] < 3.5:  # Medium (M)
                fuzzy_qoe = (3, 5, 7)
            elif QoE_metrics[i]['E[f(qos)]'] < 4.5:  # Good (G)
                fuzzy_qoe = (5, 7, 9)
            else:  # Very Good (VG)
                fuzzy_qoe = (7, 9, 9)

            # Call verification module
            # verified = Verification_module.Verification(QoE_metrics['E[f(qos)]'], rating)
            verified = Verification_module.Fuzzy_Verification(fuzzy_qoe, fuzzy_rating)
            #print("am i verified?")
            if verified:
                #print("yes,i am verified")
                # Call reputation model
                decision_matrix = list([[(1, 1, 1),
                                         (fuzzy_rating[0] / fuzzy_qoe[0], fuzzy_rating[1] / fuzzy_qoe[1],
                                          fuzzy_rating[2] / fuzzy_qoe[2])],
                                        [(fuzzy_qoe[0] / fuzzy_rating[0], fuzzy_qoe[1] / fuzzy_rating[1],
                                          fuzzy_qoe[2] / fuzzy_rating[2]), (1, 1, 1)]])

                weights = Reputation_model.Fuzzy_Reputation(decision_matrix)
                norm_weight_matrix[0][i] = weights[0]
                norm_weight_matrix[1][i] = weights[1]


            else:
                #print("no i am not verified and mismatches+=1")
                mismatches += 1
        with open(
                 'C:\\Users\\super\\Desktop\\feed4cloudProjects\\feed4cloud_weight_6\\RatingsComposition.json') as myjson_file:
             myabi = json.load(myjson_file)
        mycontract_address = '0xdEb4459c0b005956ecD102C75802FdD95f81a89f'
        mynewcontract = w3.eth.contract(address=mycontract_address, abi=myabi)

        accounts = w3.eth.accounts
        selected_account = accounts[9]
        #setting supervisor
        nonce3=w3.eth.get_transaction_count(selected_account)
        set_supervisor=mynewcontract.functions.setCredibilitySupervisor(selected_account).build_transaction(
            {
                'from': selected_account, 
                'nonce': nonce3,
                'gasPrice': w3.eth.gas_price,
                'gas': 80000
            }
        )
        gas=w3.eth.estimate_gas(
            {
                'from': selected_account, 
                'nonce': nonce3,
                'gasPrice': w3.eth.gas_price
            }
        )
        #print("Supervisor gas is")
        #print(gas)
        tx_set_supervisor = w3.eth.account.sign_transaction(set_supervisor, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77')  #second parameter is selected_account's private key
        tx_set_supervisor_hash = w3.eth.send_raw_transaction(tx_set_supervisor.rawTransaction)
        tx_set_supervisor_receipt = w3.eth.wait_for_transaction_receipt(tx_set_supervisor_hash)
        print("supervisor transaction receipt is:")
        print(tx_set_supervisor_receipt.transactionHash.hex())

        # Call credibility mechanism
        if mismatches > 3:
            qoe_data['user '] = rating['userId']
            #print("getting nonce")
            nonce1=w3.eth.get_transaction_count(selected_account)
            punish = 1
            #print("time to call setFakes function for user with id:")
            #print(rating['userId'])
            set_fakes=mynewcontract.functions.setFakes(rating['userId']).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce1,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasFakes = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce1,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("Fakes gas is")
            print(gasFakes)
            '''
            #print("i built the transaction for setfakes")
            tx_set_fakes = w3.eth.account.sign_transaction(set_fakes, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77') #to private key
            #print("i signed transaction for set_fakes")
            tx_set_fakes_hash = w3.eth.send_raw_transaction(tx_set_fakes.rawTransaction)  #edw failarei
            #print("i sent raw transaction for set fakes")
            tx_set_fakes_receipt = w3.eth.wait_for_transaction_receipt(tx_set_fakes_hash)
            print("fakes transaction receipt is:")
            print(tx_set_fakes_receipt.transactionHash.hex())
            get_fakes=mynewcontract.functions.getFakes(rating['userId']).call()
            print("for user:"+rating['userId'])
            print("fakes is:")
            print(get_fakes)
            qoe_data['fakes']=get_fakes

            nonce2=w3.eth.get_transaction_count(selected_account)
            #print("time to call getTotal function for user with id:")
            #print(rating['userId'])
            set_total=mynewcontract.functions.setTotal(rating['userId']).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce2,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasTotal = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce2,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("Total gas is")
            print(gasTotal)
            '''
            #print("i built the transaction for setfakes")
            tx_set_total = w3.eth.account.sign_transaction(set_total, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77') #to private key
            #print("i signed transaction for set_total")
            tx_set_total_hash = w3.eth.send_raw_transaction(tx_set_total.rawTransaction)  #edw failarei
            #print("i sent raw transaction for set total")
            tx_set_total_receipt = w3.eth.wait_for_transaction_receipt(tx_set_total_hash)
            print("total transaction receipt is:")
            print(tx_set_total_receipt.transactionHash.hex())
            get_total=mynewcontract.functions.getTotal(rating['userId']).call()
            print("for user:"+rating['userId'])
            print("Total is:")
            print(get_total)
            qoe_data['Total']=get_total

            #print("getting credibility rating")
            nonce2a=w3.eth.get_transaction_count(selected_account)
            #print("about to update credibility for user with ID:")
            #print(rating['userId'])
            update_Credibility_Rating=mynewcontract.functions.Credibility_rating(punish,rating['userId']).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce2a,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasCredRating = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce2a,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("CredRating gas is")
            print(gasCredRating)
            '''
            #print("i built the transaction for update credibility rating")
            tx_update_Credibility_Rating = w3.eth.account.sign_transaction(update_Credibility_Rating, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77')
            #print("i signed transaction for update_credibility rating")
            tx_update_Credibility_Rating_hash = w3.eth.send_raw_transaction(tx_update_Credibility_Rating.rawTransaction)
            #print("i didnt fail")
            tx_update_Credibility_Rating_receipt = w3.eth.wait_for_transaction_receipt(tx_update_Credibility_Rating_hash)
            print("credibility rating transaction receipt is:")
            print(tx_update_Credibility_Rating_receipt.transactionHash.hex())
            getCredibilityRating=mynewcontract.functions.getCredibilityRating(rating['userId']).call()
            print("for user:"+rating['userId'])
            print("new credibility rating is:")
            print(getCredibilityRating)
            qoe_data['credibility rating'] = getCredibilityRating

            nonce32=w3.eth.get_transaction_count(selected_account)
            #print("about to update credibility for user with ID:")
            #print(rating['userId'])
            update_Credibility=mynewcontract.functions.update_Credibility(rating['userId']).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce32,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasCredibility = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce3,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("Credibility gas is")
            print(gasCredibility)
            '''
            #print("i built the transaction for update credibility")
            tx_update_Credibility = w3.eth.account.sign_transaction(update_Credibility, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77')
            #print("i signed transaction for update_credibility")
            tx_update_Credibility_hash = w3.eth.send_raw_transaction(tx_update_Credibility.rawTransaction)
            #print("i didnt fail")
            tx_update_Credibility_receipt = w3.eth.wait_for_transaction_receipt(tx_update_Credibility_hash)
            print("credibility transaction receipt is:")
            print(tx_update_Credibility_receipt.transactionHash.hex())
            getCredibility=mynewcontract.functions.getCredibility(rating['userId']).call()
            print("for user:"+rating['userId'])
            print("new credibility is:")
            print(getCredibility)
            qoe_data['credibility'] = getCredibility
            normalised = rating['rating'] * 20
            print("normalised rating is")
            print(normalised)
            qoe_data['normalised rating'] = normalised

            nonce51=w3.eth.get_transaction_count(selected_account)
            #print("about to update reputation for user with ID:"+rating['userId'])
            update_Reputation=mynewcontract.functions.update_Reputation(rating['userId'],normalised).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce51,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasRepo = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce4,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("Reputation gas is")
            print(gasRepo)
            '''
            #print("i built the transaction for update reputation")
            tx_update_Reputation = w3.eth.account.sign_transaction(update_Reputation, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77')
            #print("i signed transaction for update_reputation")
            tx_update_Reputation_hash = w3.eth.send_raw_transaction(tx_update_Reputation.rawTransaction)
            tx_update_Reputation_receipt = w3.eth.wait_for_transaction_receipt(tx_update_Reputation_hash)
            print("reputation transaction receipt is:")
            print(tx_update_Reputation_receipt.transactionHash.hex())
            getReputation=mynewcontract.functions.getReputationScore().call()
            print("new Reputation is:")
            print(getReputation)
            qoe_data['Reputation Score'] = getReputation

        else:
            punish = 0
            qoe_data['user '] = rating['userId']
            print("write the fakes")
            get_fakes = mynewcontract.functions.getFakes(rating['userId']).call()
            qoe_data['fakes']=get_fakes

            nonce98=w3.eth.get_transaction_count(selected_account)
            print("time to call getTotal function for user with id:")
            print(rating['userId'])
            set_total=mynewcontract.functions.setTotal(rating['userId']).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce98,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasTotal = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce2,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("Total gas is")
            print(gasTotal)
            '''
            print("i built the transaction for setTotal")
            tx_set_total = w3.eth.account.sign_transaction(set_total, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77') #to private key
            print("i signed transaction for set_total")
            tx_set_total_hash = w3.eth.send_raw_transaction(tx_set_total.rawTransaction)  #edw failarei
            print("i sent raw transaction for set total")
            tx_set_total_receipt = w3.eth.wait_for_transaction_receipt(tx_set_total_hash)
            print("total transaction receipt is:")
            print(tx_set_total_receipt.transactionHash.hex())
            get_total=mynewcontract.functions.getTotal(rating['userId']).call()
            print("for user:"+rating['userId'])
            print("Total is:")
            print(get_total)
            qoe_data['Total'] = get_total

            print("getting credibility rating")
            nonce18=w3.eth.get_transaction_count(selected_account)
            punish = 0 #ara edw panta 0 to punish afou mismatches<2
            print("about to update credibility for user with ID:")
            print(rating['userId'])
            update_Credibility_Rating=mynewcontract.functions.Credibility_rating(punish,rating['userId']).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce18,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasCredRating = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce2a,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("CredRating gas is")
            print(gasCredRating)
            '''
            print("i built the transaction for update credibility rating")
            tx_update_Credibility_Rating = w3.eth.account.sign_transaction(update_Credibility_Rating, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77')
            print("i signed transaction for update_credibility rating")
            tx_update_Credibility_Rating_hash = w3.eth.send_raw_transaction(tx_update_Credibility_Rating.rawTransaction)
            print("i didnt fail")
            tx_update_Credibility_Rating_receipt = w3.eth.wait_for_transaction_receipt(tx_update_Credibility_Rating_hash)
            print("credibility rating transaction receipt is:")
            print(tx_update_Credibility_Rating_receipt.transactionHash.hex())
            getCredibilityRating=mynewcontract.functions.getCredibilityRating(rating['userId']).call()
            print("for user:"+rating['userId'])
            print("new credibility rating is:")
            print(getCredibilityRating)
            qoe_data['credibility rating'] = getCredibilityRating
        

            nonce21=w3.eth.get_transaction_count(selected_account)
            print("about to update credibility for user with ID:")
            print(rating['userId'])
            update_Credibility=mynewcontract.functions.update_Credibility(rating['userId']).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce21,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasCredibility = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce3,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("Credibility gas is")
            print(gasCredibility)
            '''
            print("i built the transaction for update credibility")
            tx_update_Credibility = w3.eth.account.sign_transaction(update_Credibility, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77')
            print("i signed transaction for update_credibility")
            tx_update_Credibility_hash = w3.eth.send_raw_transaction(tx_update_Credibility.rawTransaction)
            print("i didnt fail")
            tx_update_Credibility_receipt = w3.eth.wait_for_transaction_receipt(tx_update_Credibility_hash)
            print("credibility transaction receipt is:")
            print(tx_update_Credibility_receipt.transactionHash.hex())
            getCredibility=mynewcontract.functions.getCredibility(rating['userId']).call()
            print("for user:"+rating['userId'])
            print("new credibility is:")
            print(getCredibility)
            qoe_data['credibility'] = getCredibility

            nonce4=w3.eth.get_transaction_count(selected_account)
            print("about to update reputation for user with ID:"+rating['userId'])
            normalised=rating['rating']*20
            print("normalised rating is")
            print(normalised)
            qoe_data['normalised rating'] = normalised
            print("i wrote")
            update_Reputation=mynewcontract.functions.update_Reputation(rating['userId'],normalised).build_transaction(
                {
                    'from': selected_account,  # to address tou contract RatingsComposition
                    'nonce': nonce4,
                    'gasPrice': w3.eth.gas_price,
                    'gas': 80000
                }
            )
            '''
            gasRepo = w3.eth.estimate_gas(
                {
                    'from': selected_account, #to address tou contract RatingsComposition
                    'nonce': nonce4,
                    'gasPrice': w3.eth.gas_price
                }
            )
            print("Reputation gas is")
            print(gasRepo)
            '''
            print("i built the transaction for update reputation")
            tx_update_Reputation = w3.eth.account.sign_transaction(update_Reputation, '0xf6517cdced23a20f6c238d6f0e67d182c9feb90de1346b31105df86c0a098b77')
            print("i signed transaction for update_reputation")
            tx_update_Reputation_hash = w3.eth.send_raw_transaction(tx_update_Reputation.rawTransaction)
            tx_update_Reputation_receipt = w3.eth.wait_for_transaction_receipt(tx_update_Reputation_hash)
            print("reputation transaction receipt is:")
            print(tx_update_Reputation_receipt.transactionHash.hex())
            getReputation=mynewcontract.functions.getReputationScore().call()
            print("new Reputation is:")
            print(getReputation)
            qoe_data['Reputation Score'] = getReputation

        RTFS_repo.User.save_data()

        #dika m
        print("grafw")
        #qoe_data['user '] = rating['userId']
        #qoe_data['user credibility'] = getCredibility
        #qoe_data['Reputation Score'] = getReputation
        #qoe_data['normalised rating'] = normalised
        print("egrapsa")

        #ta palia
        #qoe_data['service QoE score'] = service.get_reputation()
        #qoe_data['user credibility'] = service_user.get_credibility()
        df = pd.DataFrame.from_dict(qoe_data)
        df = df.set_index('timestamp')
        df.index = df.index.tz_localize(pytz.utc)
        df.index = df.index.tz_convert('Europe/Athens')


        with open('qoe_data.csv', mode='a') as f:
            df.to_csv(f, header=f.tell() == 0, index_label='timestamp')


#    collector.collect_metric("Service_QoE_score", service.get_reputation())

##### REST API ######

class RTFSAPI(Resource):
    def get(self):
        return {'Trustworthy User Feedback': RTFS_repo.Feedback.load_data()}, 200  # return data and 200 OK code

    # def post(self):
    #     # headers = {"Content-Type": "application/json; charset=utf-8"}
    #     input_data = request.get_json()
    #     print(input_data)
    #     return make_response(jsonify(input_data), 200)


api.add_resource(RTFSAPI, '/rtfs')  # entry point '/rtfs'

# if __name__ == '__main__':
#     print("RTFS API is up!")
#     app.run(debug=True)  # run my locally-hosted Flask app
#
# Uncomment the following to run in parallel with Scheduler
# print("RTFS API is up!")
# app.run(debug=True)  # run my locally-hosted Flask app