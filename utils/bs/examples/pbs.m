classdef PolarizingBeamSplitter
    % PolarizingBeamSplitter - A class that simulates a Polarizing Beam Splitter (PBS).
    %
    % A PBS transmits horizontally polarized light (H) and reflects vertically polarized light (V).
    %
    % Methods:
    %   getPBSMatrix() - Returns the PBS transformation matrix.
    %   apply(inputPolarization) - Applies the PBS transformation to an input state.

    methods
        % Returns the 2x2 Jones matrix of a Polarizing Beam Splitter
        function PBS = getPBSMatrix(~)
            % The PBS matrix representation:
            % Transmits horizontal polarization: [1  0]
            % Reflects vertical polarization:    [0  i]
            PBS = [1, 0;
                  0, 1i]; % 90-degree phase shift for reflected vertical component
        end

        % Applies the Polarizing Beam Splitter to an input polarization state
        function outputPolarization = apply(obj, inputPolarization)
            % Validate that inputPolarization is a valid Jones vector
            if ~isvector(inputPolarization) || length(inputPolarization) ~= 2
                error('Input polarization must be a 2x1 Jones vector.');
            end
            
            % Get the PBS matrix
            PBS = obj.getPBSMatrix();
            
            % Apply the PBS transformation: output = PBS * input
            outputPolarization = PBS * inputPolarization;
        end
    end
end
