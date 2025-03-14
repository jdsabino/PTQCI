% Create a beam splitter with 50% transmission
bs = BeamSplitter(0.5);

% Define an input state (photon enters from port 1)
inputState = [1; 0]; % Photon is in the first input port

% Apply the beam splitter
outputState = bs.apply(inputState);

% Display the results
disp('Input State:');
disp(inputState);

disp('Output State after Beam Splitter:');
disp(outputState);
