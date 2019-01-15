% create the UGV charging map
clear all;
K=3; % number of users
M=100; % number of states
monte=1;

[K, M, states, charging_states, user_location_all, start, terminal] = environment(K, M, monte); 
% [N K h_m g_m] = channel_rician(N, K, monte); % Rician fading channel
txt = sprintf('map');
save(txt);