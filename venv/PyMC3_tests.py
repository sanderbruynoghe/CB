import numpy as np
import theano.tensor as tt
import pymc3 as pm
#import seaborn as sns
import matplotlib.pyplot as plt

#Model creation
basic_model = pm.Model() #New model: container for the model random variables

with basic_model:

    # Stochastic random variables (from a distribution)
    alpha = pm.Normal('alpha', mu=0, sigma=10) #(name, parameters): unobserved random variable
    beta = pm.Normal('beta', mu=0, sigma=10, shape=2)
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Expected value of outcome
    mu = alpha + beta[0]*X1 + beta[1]*X2 #Deterministic random variable: completely defined by parent's values

    # Likelihood (sampling distribution) of observations
    Y_obs = pm.Normal('Y_obs', mu=mu, sigma=sigma, observed=Y) #Observed random variable
