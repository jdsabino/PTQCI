classdef BeamSplitter
    % BeamSplitter - A class that simulates a beam splitter.
    %
    % A beam splitter divides an incoming light beam into a transmitted
    % and a reflected part based on a configurable transmission probability.
    %
    % Properties:
    %   T - Transmission probability (0 ≤ T ≤ 1)
    %   R - Reflection probability (automatically set as 1 - T)
    %
    % Methods:
    %   getBSMatrix() - Returns the beam splitter matrix.
    %   apply(inputState) - Applies the beam splitter to an input state.
    %   setTransmission(newT) - Updates the transmission probability.

    properties
        T % Transmission probability (0 ≤ T ≤ 1)
        R % Reflection probability (automatically computed as 1 - T)
    end

    methods
        % Constructor: Initializes the beam splitter with a given transmission probability
        function obj = BeamSplitter(T)
            % If no value is provided, default to 50% transmission
            if nargin == 0
                T = 0.5;
            end
            
            % Ensure T is within the valid range [0,1]
            if T < 0 || T > 1
                error('Transmission probability must be between 0 and 1.');
            end
            
            % Assign transmission and reflection probabilities
            obj.T = T;
            obj.R = 1 - T;
        end

        % Returns the 2x2 Beam Splitter matrix
        function BS = getBSMatrix(obj)
            % Compute the standard beam splitter matrix:
            %   [ sqrt(T)      i*sqrt(R) ]
            %   [ i*sqrt(R)    sqrt(T)   ]
            BS = [sqrt(obj.T), 1i * sqrt(obj.R);
                  1i * sqrt(obj.R), sqrt(obj.T)];
        end

        % Applies the beam splitter to an input state (Jones-like vector)
        function outputState = apply(obj, inputState)
            % Validate that inputState is a 2x1 column vector
            if ~isvector(inputState) || length(inputState) ~= 2
                error('Input state must be a 2x1 vector.');
            end
            
            % Get the beam splitter matrix
            BS = obj.getBSMatrix();
            
            % Apply the transformation: output = BS * input
            outputState = BS * inputState;
        end

        % Updates the transmission probability and adjusts reflection accordingly
        function obj = setTransmission(obj, newT)
            % Ensure newT is within the valid range [0,1]
            if newT < 0 || newT > 1
                error('Transmission probability must be between 0 and 1.');
            end
            
            % Update transmission and reflection probabilities
            obj.T = newT;
            obj.R = 1 - newT;
        end
    end
end
