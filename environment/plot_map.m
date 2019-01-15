load('map.mat')
hold on;
for m=1:M
plot(states{m}(1),states{m}(2),'ob'); % plot vertices
end

mon=1;
for k=1:K
plot(charging_states{k,mon}(:,1),charging_states{k,mon}(:,2),'squarer','MarkerSize',15); % plot vertices
end

plot(start(1),start(2),'k*');
plot(terminal(1),terminal(2),'k*');
