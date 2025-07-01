close all
clc

% === CONFIGURE PATH ===
log_file = 'LogL.txt';

% === READ FILE ===
fid = fopen(log_file, 'r');
lines = textscan(fid, '%s', 'Delimiter', '\n');
fclose(fid);
lines = lines{1};

% === INIT VARIABLES ===
timestamps = {};
gain = []; et = []; Bv = []; Ev = []; PEv = []; lux = []; drc = []; PHdr = [];

% === REGEX PATTERN (MATCHES PYTHON) ===
pattern = ['(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*?' ...
           'g=([\d.]+),e_t=([\d.]+),Bv=([-.\d]+),Ev=([-.\d]+),PEv=([-.\d]+),.*?' ...
           'lux=(\d+),.*?drc=([\d.]+),PHdr=([\d.]+)'];

% === EXTRACT DATA ===
for i = 1:length(lines)
    tokens = regexp(lines{i}, pattern, 'tokens');
    if ~isempty(tokens)
        t = tokens{1};
        timestamps{end+1} = t{1};
        gain(end+1) = str2double(t{2});
        et(end+1) = str2double(t{3});
        Bv(end+1) = str2double(t{4});
        Ev(end+1) = str2double(t{5});
        PEv(end+1) = str2double(t{6});
        lux(end+1) = str2double(t{7});
        drc(end+1) = str2double(t{8});
        PHdr(end+1) = str2double(t{9});
    end
end

% === CONVERT TO TABLE ===
timeVec = datetime(timestamps, 'InputFormat', 'yyyy-MM-dd HH:mm:ss.SSSSSS');
T = table(timeVec', gain', et', Bv', Ev', PEv', lux', drc', PHdr', ...
    'VariableNames', {'timestamp','gain','et','Bv','Ev','PEv','lux','drc','PHdr'});

% === CALCULATE DIFFERENCES ===
T.Ev_diff = [NaN; diff(T.Ev)];

% === PLOT PHdr ===
figure('Position', [100 100 1000 500]);
subplot(1,2,1)
plot(T.timestamp, T.PHdr, '-o', 'Color', [0.427, 0.349, 0.478], 'LineWidth', 2, 'DisplayName', 'PHdr');
xlabel('Timestamp');
ylabel('PHdr');
grid on;
xtickformat('yyyy-MM-dd HH:mm:ss');
xticks(linspace(min(T.timestamp), max(T.timestamp), 10));
xtickangle(45);
legend('Location', 'northeast');

subplot(1,2,2)
plot(T.timestamp, T.drc, '-o', 'Color', [79  109 122]/255, 'LineWidth', 2, 'DisplayName', 'DRC');
xlabel('Timestamp');
ylabel('Dynamic Range Compression');
grid on;
xtickformat('yyyy-MM-dd HH:mm:ss');
xticks(linspace(min(T.timestamp), max(T.timestamp), 10));
xtickangle(45);
legend('Location', 'northeast');

sgtitle('S25 Dark Setting')
set(gcf, 'Color', 'white');

%% ========================================================================
% ---------------------- Motorola -----------------------------------------
clc
close all

% === CONFIGURE FILE ===
log_file = 'Moto5GP_bright.txt';

if ~isfile(log_file)
    error('File not found: %s', log_file);
end

% === READ FILE ===
fid = fopen(log_file, 'r');
lines = textscan(fid, '%s', 'Delimiter', '\n');
fclose(fid);
lines = lines{1};

% === INIT STORAGE ===
exposure_time = [];
timestamp_strings = {};

% === REGEX TO EXTRACT TIMESTAMP AND u4Eposuretime ===
pattern = '(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*?u4Eposuretime:(\d+)';
for i = 1:length(lines)
    tokens = regexp(lines{i}, pattern, 'tokens');
    if ~isempty(tokens)
        timestamp_strings{end+1} = tokens{1}{1};
        exposure_time(end+1) = str2double(tokens{1}{2});
    end
end

% === CONVERT TIMESTAMP TO datetime ===
try
    dt = datetime(timestamp_strings, 'InputFormat', 'MM-dd HH:mm:ss.SSS');
    dt.Year = year(datetime('now'));
catch
    error('Datetime conversion failed. Check timestamp format.');
end

% === CONFIRM DATETIME RULER ===
if ~isa(dt, 'datetime') || isempty(dt)
    error('Datetime conversion failed or dt is empty.');
end

% === PLOT ===
figure;
subplot(1,2,1)
plot(dt, exposure_time, '-o', 'LineWidth', 2, 'Color',  [0.0824, 0.5176, 0.5608]);
xlabel('Timestamp');
ylabel('u4Eposuretime');
title('Moto 5G Power Bright Setting')
grid on;

% === FORMAT TICKS SAFELY ===
ax = gca();
if isa(ax, 'matlab.graphics.axis.Axes') && isa(ax.XAxis, 'matlab.graphics.axis.decorator.DatetimeRuler')
    ax.XAxis.TickLabelFormat = 'HH:mm:ss.SSS';
end
xtickangle(ax, 45);

set(gcf, 'Color', 'white');


% === CONFIGURE FILE ===
log_file = 'Moto5GP_dark.txt';

if ~isfile(log_file)
    error('File not found: %s', log_file);
end

% === READ FILE ===
fid = fopen(log_file, 'r');
lines = textscan(fid, '%s', 'Delimiter', '\n');
fclose(fid);
lines = lines{1};

% === INIT STORAGE ===
exposure_time = [];
timestamp_strings = {};

% === REGEX TO EXTRACT TIMESTAMP AND u4Eposuretime ===
pattern = '(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*?u4Eposuretime:(\d+)';
for i = 1:length(lines)
    tokens = regexp(lines{i}, pattern, 'tokens');
    if ~isempty(tokens)
        timestamp_strings{end+1} = tokens{1}{1};
        exposure_time(end+1) = str2double(tokens{1}{2});
    end
end

% === CONVERT TIMESTAMP TO datetime ===
try
    dt = datetime(timestamp_strings, 'InputFormat', 'MM-dd HH:mm:ss.SSS');
    dt.Year = year(datetime('now'));
catch
    error('Datetime conversion failed. Check timestamp format.');
end

% === CONFIRM DATETIME RULER ===
if ~isa(dt, 'datetime') || isempty(dt)
    error('Datetime conversion failed or dt is empty.');
end

% === PLOT ===
subplot(1,2,2)
plot(dt, exposure_time, '-o', 'LineWidth', 2, 'Color',  [0.0824, 0.5176, 0.5608]);
xlabel('Timestamp');
ylabel('u4Eposuretime');
title('Moto 5G Power Dark Setting')
grid on;

% === FORMAT TICKS SAFELY ===
ax = gca();
if isa(ax, 'matlab.graphics.axis.Axes') && isa(ax.XAxis, 'matlab.graphics.axis.decorator.DatetimeRuler')
    ax.XAxis.TickLabelFormat = 'HH:mm:ss.SSS';
end
xtickangle(ax, 45);

set(gcf, 'Color', 'white');