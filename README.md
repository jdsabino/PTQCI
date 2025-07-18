# Purpose
These codes are supposed to implement the quantum source and detection mechanisms for the Hardware-in-the-loop (HIL) simulator being developed for task 4.5 of PTQCI project.
The code that simulates the source is in file qtx.py, while the remaining files consist of useful functions (like "dist_random_values") or matlab code to simulate the detectors and optical elements like beamsplitters or waveplates.
Below we describe the most important points about the quantum photon source and detectors.

# Quantum photon source
The qtx.py file simulates a photon source taylored for the decoy state BB84 protocol.
The output of the code is an array stating how many photons were emitted in each 'event' (definition of event coming soon) and a second array stating the quantum state of the emitted photons for the corresponding event.

An event corresponds to the smallest duration that the event-based simulation considers. If the HIL simulator considers a time step of 1 ms, then we consider that there is an event for each ms. The same would happen if instead 1ms we used 1ns. If that was the case, we would have more events for the same simulation duration.
The first task that this piece of code does is precisely calculating how many events we need to simulate, provided that the simulation precision ('src_clock') and simulation duration is known.

Regarding state generation, the code takes in the mean photon value per pulse for regular states (used for key generation), decoy states (to detect the eavesdropper) and vaccum state. To each of these different pulse types, a coherent state with the corresponding mean photon number is assinged.
These mean photon numbers will allow to calculate the probability (and to do sampling) of how many photons will be emitted in a specific event (=specific time).  


# Detectors
