import numpy as np
import qutip as qtp
import matplotlib.pyplot as plt
import time
from dist_random_values import dist_random_values

###--- Variables
t0 = time.time()
# Time definitions
sim_clock = 1
src_clock = 1e-6
sim_time  = 5*sim_clock

Nevents = int(sim_time/src_clock)

# Source definitions
# ###--- Laser intensities (average number of phtons per pulse)
muS = 0.6
muD = 0.1
muV = 0.005

mus = np.array([muS, muD, muV])

# ###--- Probability of signal, decoy and vacuum states
pD = 0.1
pV = 0.005
pS = 1 - pD - pV

probs = np.array([pS, pD, pV])


###--- Generate basis, plarizations and intensities

# Polarizations
pols = np.random.randint(0, high=2, size=Nevents) # Generates string of zeros and ones to choose one of the polarizatoins in each basis

basis_pol = np.random.randint(0, high=2, size=Nevents) # Generates string of zeros and ones to choose the basis (convention: 0-HV, 1-AD)

intensities = np.random.uniform(size=Nevents)


#--- New way - The 'dist_random_values' way:
intensities = dist_random_values(Nevents, mus, probs)
unique, counts = np.unique(intensities, return_counts=True)
val_cnt = np.array([len(intensities[intensities == mu]) for mu in mus])

###--- Generate the coherent states
dim = 6 # Fock state dimnsion

# # Vaccum Coherent State
# alpha = np.sqrt(muV) # alpha could be complex but I'm keeping it simple for now
# stateV = qtp.coherent(dim, alpha)

# # Decoy Coherent State
# alpha = np.sqrt(muD) # alpha could be complex but I'm keeping it simple for now
# stateD = qtp.coherent(dim, alpha)

# # Signal Coherent State
# alpha = np.sqrt(muS) # alpha could be complex but I'm keeping it simple for now
# stateS = qtp.coherent(dim, alpha)


###--- Compute how many photons we will have on each instant
"""
For this, I will check how many times we have to measure each coherent state
(that is how many light pulses with different mus we have) abd measure the
coherent states that many times. This will give us the amount of photons for each pulse.
"""

measurement_ops = [qtp.ket2dm(qtp.basis(dim, _)) for _ in range(dim)]

alpha = np.array([qtp.coherent(dim, mu) for mu in  mus])
measure_probs = [qtp.measurement.measurement_statistics_povm(state, measurement_ops)[1] for state in alpha]

# stats = [np.array(list(zip(range(dim), measure))) for measure in measure_probs]

#val_cnt = np.array([len(intensities[intensities == mu]) for mu in mus])
results = [dist_random_values(val_cnt[idx], np.arange(dim), np.array(measure_probs[idx])) for idx in range(len(measure_probs))]

nphotons = np.zeros(intensities.shape)

for idx, res in enumerate(results):
    nphotons[np.where(intensities==mus[idx])[0]] = res
    # nphotons[np.where(intensities==unique[idx])[0]] = res


### Generate polarization states - TODO
polH = np.array([[1], [0]])#qtp.basis(2, 0)
polV = np.array([[0], [1]])#qtp.basis(2, 1)

def gen_pol_state(basis, pol):

    return (1-basis)*((1-pol)*polH + pol*polV) + basis*((1-pol)*(polH+polV) + pol*(polH - polV))/np.sqrt(2)

random_photons = np.concatenate((basis_pol.reshape(Nevents,1), pols.reshape(Nevents,1)), axis=1)

pol_states =(1-basis_pol)*((1-pols)*polH + pols*polV) + basis_pol*((1-pols)*(polH+polV) + pols*(polH - polV))/np.sqrt(2)#  [gen_pol_state(choice[0], choice[1]) for choice in random_photons]

pol_states = pol_states.transpose() # First dimension is associated with events, second is polarizarion.

save_data = np.concatenate((nphotons.reshape(nphotons.shape[0],1), pol_states), axis=1)

np.savetxt("photon_pulses.txt", save_data)

t1 = time.time()

print("Simulation took " + str(t1 - t0) + " seconds to run.")



# Control Report

print("Pulse percentage: ")
print("muS: " + str(val_cnt[0]/Nevents))
print("muD: " + str(val_cnt[1]/Nevents))
print("muV: " + str(val_cnt[2]/Nevents))

def poisson(mu, kk):
    from scipy.special import factorial
    return (mu**kk)*np.exp(-mu)/factorial(kk)

xx = np.linspace(0, dim)
poiV = poisson(muV, xx)
poiD = poisson(muD, xx)
poiS = poisson(muS, xx)



plt.rcParams['text.usetex'] = True
height = 0.8 # heigh of text in plot


fig, axs = plt.subplots(2, 3)
axs[0, 0].plot(xx, poiV*Nevents, '--r')
vals, bins, bars = axs[0, 1].hist(results[2], bins=[0,1,2,3,4,5])
axs[0, 0].set_ylabel(r"Absolute frequency")
axs[0, 0].set_ylim((0, Nevents*muS))
axs[0, 0].bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
axs[0, 0].text(dim/2, height*muS*Nevents, r"$\mu = " + str(muV) + "$")
# plt.yscale("log")

#--- Vaccum pulses dist

axs[0, 1].plot(xx, poiD*Nevents, '--r')
vals, bins, bars = axs[0, 1].hist(results[1], bins=[0,1,2,3,4,5])
axs[0, 1].set_ylim((0, Nevents*muS))
axs[0, 1].set_xlabel(r"\# photons")
axs[0, 1].set_yticks([])
axs[0, 1].bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
axs[0, 1].text(dim/2, height*muS*Nevents, r"$\mu = " + str(muD) + "$")
# plt.yscale("log")

#--- Vaccum pulses dist

axs[0, 2].plot(xx, poiS*Nevents, '--r')
vals, bins, bars = axs[0, 2].hist(results[0], bins=[0,1,2,3, 4, 5])
axs[0, 2].set_ylim((0, Nevents*muS))
axs[0, 2].set_yticks([])
axs[0, 2].bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
axs[0, 2].text(dim/2, height*muS*Nevents, r"$\mu = " + str(muS) + "$")
# plt.yscale("log")

gs = axs[1, 2].get_gridspec()

for ax in axs[1, :]:
    ax.remove()

axbig = fig.add_subplot(gs[1, :])
axbig.plot(np.linspace(0, sim_time, Nevents), nphotons,  'og', markersize=0.1)
axbig.set_ylabel("Emitted photons")
axbig.set_xlabel("Time (sim clock units)")
plt.show()




