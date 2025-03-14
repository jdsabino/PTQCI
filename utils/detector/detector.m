classdef SinglePhotonCounter
    properties
        detectionProbability % Probability of detecting an incoming photon
        darkCountRate % Average dark count rate (in counts per second)
        deadTime % Dead time after each detection (in seconds)
    end

    properties (Access = private)
        lastDetectionTime % Time of the last detection to handle dead time
    end

    methods
        % Constructor to initialize the class
        function obj = SinglePhotonCounter(detectionProbability, darkCountRate, deadTime)
            obj.detectionProbability = detectionProbability;
            obj.darkCountRate = darkCountRate;
            obj.deadTime = deadTime;
            obj.lastDetectionTime = -inf; % Initializing to a very old time
        end

        % Method to simulate a single photon detection
        % Parameters:
        %   currentTime - the current time in seconds
        %   photonIncoming - logical indicating if a photon arrives
        % Returns:
        %   detected - logical indicating if the photon was detected
        function detected = detectPhoton(obj, currentTime, photonIncoming)
            % Initialize detected status to false
            detected = false;

            % Check if we are within dead time
            if currentTime - obj.lastDetectionTime < obj.deadTime
                return; % Detector is in dead time, no detection possible
            end

            % Check if a photon is incoming and detection occurs based on probability
            if photonIncoming && (rand() < obj.detectionProbability)
                detected = true;
            elseif rand() < obj.darkCountRate * (currentTime - obj.lastDetectionTime)
                % Simulate dark count as a random event
                detected = true;
            end

            % Update last detection time if a detection occurred
            if detected
                obj.lastDetectionTime = currentTime;
            end
        end

        % Method to simulate photon detections over a time period
        % Parameters:
        %   timeVector - vector of time points (in seconds)
        %   photonStream - vector of logicals (1 if a photon arrives, 0 if not)
        % Returns:
        %   detectionEvents - vector of logicals (1 if detection occurs, 0 if not)
        function detectionEvents = simulateDetection(obj, timeVector, photonStream)
            numTimePoints = length(timeVector);
            detectionEvents = false(1, numTimePoints);

            % Loop through each time point to check for detections
            for i = 1:numTimePoints
                detectionEvents(i) = obj.detectPhoton(timeVector(i), photonStream(i));
            end
        end

        % New method: Perform a single detection manually
        % Parameters:
        %   photonIncoming - logical indicating if a photon arrives
        % Returns:
        %   detected - logical indicating if the photon was detected
        function detected = singleDetection(obj, photonIncoming)
            % Get the current time (simulation time)
            currentTime = tic; % Get high-resolution current time in seconds

            % Call the detectPhoton method with the current time
            detected = obj.detectPhoton(currentTime, photonIncoming);
        end
    end
end
