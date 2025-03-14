% Create an HWP with a 22.5° rotation
hwp22_5 = HalfWavePlate(22.5);

% Input: 45-degree linear polarization
inputPol = [1; 1] / sqrt(2);

% Apply HWP transformation
outputPol = hwp22_5.apply(inputPol);

% Display result
disp('Rotated Polarization:');
disp(outputPol);
