# MMSBMrecommender
Code and files for the social recommendation mixed-membership stochastic block model algorithm (article https://www.pnas.org/content/113/50/14207). 
The code is written in Pypy (a Python interpreter)---you can use python just changing 'import _numpypy as np' by 'import numpy as np'. To run the code:
pypy mmsbm_recommender.py training_dataset test_dataset K L (sampling iterations)

where K is the number of group-memberships for users and L is the number of group memberships for items. "(sampling iterations)" are optional parameters. Default values are 1 for sampling and 200 for iterations.

The algorithm gives slightly different solutions depending on the initialization of the parameters. As none of these solutions is significantly better than the other we perform different random initializations ('sampling' in the code), and the final probability distribution over the ratings is the average over all of them.
We suggest distributing the sampling process, given that they are independent processes which speed up the computation. For the iterations, fixing the iterations save computational time, but to fix the value ensure that likelihood is in a plateau. You can compute the likelihood from time to time to stop the iterations when the likelihood is not growing, but it also takes computational time.

The output file with predictions is 'predictions.dat':
userID itemID real_rating prediction_rating ratings_probability_distribution
