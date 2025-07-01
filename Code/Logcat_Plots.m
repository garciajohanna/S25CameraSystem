close all
clc

% === CONFIGURE PATH ===
log_file = 'Test.txt';

% === READ FILE ===
lines = readlines(log_file);

% === INITIALIZE STORAGE ===
timestamps = datetime.empty;
frame_numbers = [];

% === PARSE AND PRINT ===

for i = 1:length(lines)
    line = lines(i);

    match = regexp(line, ...
        '^(?<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*mFrameNumber\s+(\d+)', ...
        'tokens');

    if ~isempty(match)
        fprintf('%s\n', line);
        ts = datetime(match{1}{1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss.SSS');
        fr = str2double(match{1}{2});

        timestamps(end+1) = ts;
        frame_numbers(end+1) = fr;
    end
end

% === PLOT: Timestamp vs Frame Number ===
figure;
plot(timestamps, frame_numbers, 'o-');
xlabel('Timestamp');
ylabel('Frame Number');
title('Timestamp vs Frame Number (from mFrameNumber)');
grid on;