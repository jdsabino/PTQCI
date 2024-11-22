import numpy as np
import qutip as qtp
import matplotlib.pyplot as plt
import time

###--- Variables
t0 = time.time()
# Time definitions
sim_clock = 1
src_clock = 1e-3
sim_time  = 5*sim_clock

Nevents = int(sim_time/src_clock)

# Source definitions
# ###--- Laser intensities (average number of phtons per pulse)
muS = 0.6
muD = 0.1
muV = 0.005

# ###--- Probability of signal, decoy and vacuum states
pV = 0.005
pD = 0.1
pS = 1 - pD - pV 


###--- Generate basis, plarizations and intensities

# Polarizations
pols = np.random.randint(0, high=2, size=Nevents) # Generates string of zeros and ones to choose one of the polarizatoins in each basis

basis_pol = np.random.randint(0, high=2, size=Nevents) # Generates string of zeros and ones to choose the basis (convention: 0-HV, 1-AD)


intensities = np.random.uniform(size=Nevents)

# Vacuum intensities
indexV = np.where(intensities <= pV)[0]
totV = indexV.shape[0] # Total number of Vaccuum states
intensities[indexV] = muV

# Decoy intensities
indexD = np.where(np.logical_and(intensities > pV, intensities <= pD+pV))[0]
totD = indexD.shape[0] # Total number of Decoy states
intensities[indexD] = muD

# Signal intensities
indexS = np.where(intensities > pD+pV)[0]
totS = indexS.shape[0] # Total number of Signal states
intensities[indexS] = muS



###--- Generate the coherent states
dim = 5 # Fock state dimnsion

# Vaccum Coherent State
alpha = np.sqrt(muV) # alpha could be complex but I'm keeping it simple for now
stateV = qtp.coherent(dim, alpha)

# Decoy Coherent State
alpha = np.sqrt(muD) # alpha could be complex but I'm keeping it simple for now
stateD = qtp.coherent(dim, alpha)

# Signal Coherent State
alpha = np.sqrt(muS) # alpha could be complex but I'm keeping it simple for now
stateS = qtp.coherent(dim, alpha)


###--- Compute how many photons we will have on each instant
"""
For this, I will check how many times we have to measure each coherent state
(that is how many light pulses with different mus we have) abd measure the
coherent states that many times. This will give us the amount of photons for each pulse.
"""

# Generate measurement operators
measurement_ops = [qtp.ket2dm(qtp.basis(dim, _)) for _ in range(dim)]

#resultV, _ = qtp.measurement.measure(stateV, measurement_ops)
resultV = np.array([qtp.measurement.measure(stateV, measurement_ops)[0] for res in range(0, totV)])
#resultD, _ = qtp.measurement.measure(stateD, measurement_ops)
resultD = np.array([qtp.measurement.measure(stateD, measurement_ops)[0] for res in range(0, totD)])
#resultS, _ = qtp.measurement.measure(stateS, measurement_ops)
resultS = np.array([qtp.measurement.measure(stateS, measurement_ops)[0] for res in range(0, totS)])

nphotons = np.zeros(intensities.shape)

nphotons[indexV] = resultV
nphotons[indexD] = resultD
nphotons[indexS] = resultS

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
print("muS: " + str(len(indexS)/Nevents))
print("muD: " + str(len(indexD)/Nevents))
print("muV: " + str(len(indexV)/Nevents))

def poisson(mu, kk):
    from scipy.special import factorial
    return (mu**kk)*np.exp(-mu)/factorial(kk)

xx = np.linspace(0, dim)
poiV = poisson(muV, xx)
poiD = poisson(muD, xx)
poiS = poisson(muS, xx)



plt.rcParams['text.usetex'] = True
height = 0.8 # heigh of text in plot
#--- Vaccum pulses dist
# plt.subplot(1, 3, 1)
# plt.plot(xx, poiV*Nevents, '--r')
# vals, bins, bars = plt.hist(resultV, bins=[0,1,2,3,4,5])
# plt.ylabel(r"Absolute frequency")
# plt.ylim((0, Nevents*muS))
# plt.bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
# plt.text(dim/2, height*muS*Nevents, r"$\mu = " + str(muV) + "$")
# # plt.yscale("log")

# #--- Vaccum pulses dist
# plt.subplot(1, 3, 2)
# plt.plot(xx, poiD*Nevents, '--r')
# vals, bins, bars = plt.hist(resultD, bins=[0,1,2,3,4,5])
# plt.ylim((0, Nevents*muS))
# plt.xlabel(r"\# photons")
# plt.yticks([])
# plt.bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
# plt.text(dim/2, height*muS*Nevents, r"$\mu = " + str(muD) + "$")
# # plt.yscale("log")

# #--- Vaccum pulses dist
# plt.subplot(1, 3, 3)
# plt.plot(xx, poiS*Nevents, '--r')
# vals, bins, bars = plt.hist(resultS, bins=[0,1,2,3, 4, 5])
# plt.ylim((0, Nevents*muS))
# plt.yticks([])
# plt.bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
# plt.text(dim/2, height*muS*Nevents, r"$\mu = " + str(muS) + "$")
# # plt.yscale("log")


fig, axs = plt.subplots(2, 3)
axs[0, 0].plot(xx, poiV*Nevents, '--r')
vals, bins, bars = axs[0, 1].hist(resultV, bins=[0,1,2,3,4,5])
axs[0, 0].set_ylabel(r"Absolute frequency")
axs[0, 0].set_ylim((0, Nevents*muS))
axs[0, 0].bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
axs[0, 0].text(dim/2, height*muS*Nevents, r"$\mu = " + str(muV) + "$")
# plt.yscale("log")

#--- Vaccum pulses dist

axs[0, 1].plot(xx, poiD*Nevents, '--r')
vals, bins, bars = axs[0, 1].hist(resultD, bins=[0,1,2,3,4,5])
axs[0, 1].set_ylim((0, Nevents*muS))
axs[0, 1].set_xlabel(r"\# photons")
axs[0, 1].set_yticks([])
axs[0, 1].bar_label(bars, fontsize= 10, color=[0,0,0,0.5])
axs[0, 1].text(dim/2, height*muS*Nevents, r"$\mu = " + str(muD) + "$")
# plt.yscale("log")

#--- Vaccum pulses dist

axs[0, 2].plot(xx, poiS*Nevents, '--r')
vals, bins, bars = axs[0, 2].hist(resultS, bins=[0,1,2,3, 4, 5])
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




###--- TODO
# - Write function dist_random_values([v1,v2,...,vn], [p1, p2, ..., pn])
# - test times
