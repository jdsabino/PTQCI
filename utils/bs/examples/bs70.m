% Create a beam splitter with 70% transmission
bs70 = BeamSplitter(0.7);

% Input: Photon in port 1
inputPhoton = [1; 0];

% Apply the beam splitter
outputPhoton = bs70.apply(inputPhoton);

% Display results
disp('Output with 70% transmission:');
disp(outputPhoton);
