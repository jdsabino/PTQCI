classdef HalfWavePlate
    % HalfWavePlate - A class that simulates a Half-Wave Plate (HWP).
    %
    % This class models the behavior of a Half-Wave Plate, which rotates 
    % the polarization of light by an amount that depends on the angle of 
    % its fast axis. The polarization rotation is **twice** the angle of 
    % the HWP's fast axis.
    %
    % Properties:
    %   theta - The angle of the fast axis of the HWP (in degrees). 
    %           This determines the polarization rotation.
    %
    % Methods:
    %   getJonesMatrix() - Returns the Jones matrix representing the HWP.
    %   apply(inputPolarization) - Applies the HWP transformation to an 
    %                              input polarization state (Jones vector).
    %   setTheta(newTheta) - Updates the angle of the fast axis.
    
    properties
        theta % Rotation angle of the fast axis (in degrees)
    end
    
    methods
        % Constructor: Initializes the Half-Wave Plate with a given angle
        function obj = HalfWavePlate(theta)
            % If no angle is provided, default to 0 degrees
            if nargin == 0
                theta = 0;
            end
            
            % Ensure the angle stays within the range [0, 360] degrees
            obj.theta = mod(theta, 360);
        end
        
        % Returns the Jones matrix representation of the Half-Wave Plate
        function H = getJonesMatrix(obj)
            % Convert angle from degrees to radians
            theta_rad = deg2rad(obj.theta);
            
            % Compute the Jones matrix for the HWP:
            % HWP introduces a phase shift such that:
            %   H(theta) = [ cos(2θ)   sin(2θ) ]
            %              [ sin(2θ)  -cos(2θ) ]
            H = [cos(2 * theta_rad), sin(2 * theta_rad);
                 sin(2 * theta_rad), -cos(2 * theta_rad)];
        end
        
        % Applies the Half-Wave Plate transformation to an input polarization state
        function outputPolarization = apply(obj, inputPolarization)
            % Validate that inputPolarization is a valid Jones vector
            if ~isvector(inputPolarization) || length(inputPolarization) ~= 2
                error('Input polarization must be a 2x1 Jones vector.');
            end
            
            % Get the HWP transformation matrix
            H = obj.getJonesMatrix();
            
            % Apply the transformation: output = H * input
            outputPolarization = H * inputPolarization;
        end
        
        % Updates the rotation angle of the Half-Wave Plate
        function obj = setTheta(obj, newTheta)
            % Ensure the angle stays within [0, 360] degrees
            obj.theta = mod(newTheta, 360);
        end
    end
end
