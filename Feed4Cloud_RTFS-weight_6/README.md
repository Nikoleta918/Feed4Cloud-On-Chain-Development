# Feed4Cloud

This reporitory hosts the RatingBlock Trusted Feedback System (RTFS), developed during the Feed4Cloud project (funded by the TruBlo Open Call #3).

The Feed4Cloud project aims to effectively tackles the problem of collecting QoE-related user-generated feedback for cloud-native services in a transparent and trustworthy manner. By integrating credible user feedback, the Feed4Cloud solution offers an enhanced cloud monitoring framework.

RTFS, particularly, supports the following operations: 

1. Calculcation of the expected user rating by using the IQX hypothesis as QoS-to-QoE mapping algorithm (implemented in the 'QoSQoEmapper.py'). Such mapping is implemented based on the open-source repository: https://github.com/hossfeld/approx-qoe-distribution
2. User-generated feedback verification (implemented in the 'Verification_module.py'). 
3. User credibility assessment (implemented in the 'Credibility_mechanism.py')
4. Service evaluation (implemented in the 'Reputation_model.py')

RTFS.py gets real-time QoS data from a Netdata monitoring agent using the 'requests' library, while also interacts with the Feed4Cloud designated smart contract to retrieve user ratings recorded in a Blockchain client.