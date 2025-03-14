% Create a Polarizing Beam Splitter
pbs = PolarizingBeamSplitter();

% Define an input polarization state (45-degree polarization)
inputPolarization = [1; 1] / sqrt(2);

% Apply the PBS transformation
outputPolarization = pbs.apply(inputPolarization);

% Display the results
disp('Input Polarization:');
disp(inputPolarization);

disp('Output Polarization after PBS:');
disp(outputPolarization);
