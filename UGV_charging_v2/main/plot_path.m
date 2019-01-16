load('example.mat');

%% generate the map
mon=path;
hold on;
% plot starting point
p0=plot(states{1}(1),states{1}(2),'ob','MarkerSize',15);
for m=1:M
% plot all vertices
p1=plot(states{m}(1),states{m}(2),'ksquare','MarkerSize',8);
end

for r=1:length(charging_states)
    % plot charging regions
    for i=1:size(charging_states{r},1)
        p2=plot(charging_states{r}(i,1),charging_states{r}(i,2),'+r','MarkerSize',r*10);
    end
end

v1=v1_all(:,mon);
x1=x1_all(:,:,mon);

% plot proposed
for m=1:M
    for j=1:M
        if x1(m,j)>0.5
            p4=plot([states{m}(1), states{j}(1)],[states{m}(2), states{j}(2)],'-k','LineWidth',2);
        end
    end
end

legend([p0,p1,p2,p4],'Starting point','Vertices','Charging region','Proposed');

