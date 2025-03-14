% Create a Polarizing Beam Splitter
pbs = PolarizingBeamSplitter();

% Horizontally Polarized Photon (H)
inputH = [1; 0]; % Pure H polarization
outputH = pbs.apply(inputH);

% Vertically Polarized Photon (V)
inputV = [0; 1]; % Pure V polarization
outputV = pbs.apply(inputV);

% Display the results
disp('--- Horizontally Polarized Photon ---');
disp('Input:');
disp(inputH);
disp('Output: (Should be unchanged)');
disp(outputH);

disp('--- Vertically Polarized Photon ---');
disp('Input:');
disp(inputV);
disp('Output: (Should have a 90-degree phase shift)');
disp(outputV);
