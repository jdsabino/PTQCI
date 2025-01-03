% Parameters
detectionProbability = 0.6; % 60% probability to detect incoming photons
darkCountRate = 10; % 10 dark counts per second
deadTime = 1e-6; % 1 microsecond dead time

% Create the photon counter object
spcm = SinglePhotonCounter(detectionProbability, darkCountRate, deadTime);

% Simulation time vector (e.g., 1 ms in 1 ns intervals)
timeVector = 0:1e-9:1e-3; % 1 ns intervals over 1 ms

% Simulated photon stream (50 photons randomly spread out)
photonStream = rand(1, length(timeVector)) < 50 / length(timeVector);

% Run the simulation
detectionEvents = spcm.simulateDetection(timeVector, photonStream);

% Plot the results
figure;
plot(timeVector, photonStream, 'b', 'DisplayName', 'Incoming Photons');
hold on;
plot(timeVector, detectionEvents, 'r', 'DisplayName', 'Detected Photons');
legend;
xlabel('Time (s)');
ylabel('Photon Signal');
title('Photon Detection Simulation');
