% Create a Half-Wave Plate with a 45-degree fast axis
hwp = HalfWavePlate(45);

% Define an input polarization state (Jones vector)
% Example: Horizontally polarized light [1; 0]
inputPolarization = [1; 0];

% Apply the HWP to transform the polarization
outputPolarization = hwp.apply(inputPolarization);

% Display the results
disp('Input Polarization:');
disp(inputPolarization);

disp('Output Polarization after HWP:');
disp(outputPolarization);
