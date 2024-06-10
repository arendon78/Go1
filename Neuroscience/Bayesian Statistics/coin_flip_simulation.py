import numpy as np
import matplotlib.pyplot as plt


N = 1000 # Number of flips
BIAS_HEADS = 0.5 # The bias of the coin

bias_range = np.linspace(0, 1, 101) # The range of possible biases

# Giving all hypotheses the same weight
#prior_bias_heads = np.ones(len(bias_range)) / len(bias_range) # Uniform prior distribution

# Assuming certain hypothesis has more weight
mu, sigma = 0.1, 0.25
prior_bias_heads = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bias_range - mu)**2 / (2 * sigma**2) )

flip_series = (np.random.rand(N) <= BIAS_HEADS).astype(int) # A series of N 0's and 1's (coin flips)

i = 0
for flip in flip_series:
    likelihood = bias_range**flip * (1-bias_range)**(1-flip)
    evidence = np.sum(likelihood * prior_bias_heads)
    prior_bias_heads = likelihood * prior_bias_heads / evidence

#    if i == 10 or i == 20 or i == 30 or i == 40 or i == 50 or i == 60 or i == 70 or i == 80 or i == 90 or i == 100:
#        plt.plot(bias_range, prior_bias_heads)
#        plt.xlabel('Heads Bias')
#        plt.ylabel('P(Heads Bias)')
#        plt.grid()
#        plt.pause(0.1)
#        print("Evidence " + str(i) + ":" + str(evidence))

    i += 1

#plt.show()

plt.plot(bias_range, prior_bias_heads)
plt.xlabel('Heads Bias')
plt.ylabel('P(Heads Bias)')
plt.grid()
plt.show()
print("Evidence " + str(i) + ":" + str(evidence))

'''
prior_bias_heads = 0.1
flip_series = (np.random.rand(N) <= BIAS_HEADS).astype(int) # A series of N 0's and 1's (coin flips)

print(flip_series)

for flip in flip_series:
    likelihood = prior_bias_heads**flip * (1-prior_bias_heads)**(1-flip)
    evidence = likelihood * prior_bias_heads + likelihood * (1-prior_bias_heads)

    print("**********")
    print("Flip: " + str(flip))
    print("Prior belief: " + str(prior_bias_heads))
    print("Likelihood: " + str(likelihood))
    print("Evidence: " + str(evidence))

    prior_bias_heads = likelihood * prior_bias_heads / evidence
    print("New belief: " + str(prior_bias_heads))

#print("New belief: " + str(prior_bias_heads))
'''