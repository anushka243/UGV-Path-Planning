clear all;
% Information for the platform
disp('***** This platform is used to simulate the MINLP algorithm.');
load('map.mat')

terminal=64; % back to the starting point
% registers
v1_all=zeros(M,monte);
x1_all=zeros(M,M,monte);
v2_all=zeros(M,monte);
x2_all=zeros(M,M,monte);

path=1; % channel index
monte=path;
fprintf('Starting simulating path......');
for mon = monte: monte
    if mod(mon,50)==0
        disp('50 monte carlo finished!');
    end
    
    [E1, v1, x1]= proposed(K, M, D, terminal(mon), charging_index);
%     [E2, v2, x2] = shortestpath(K, M, D, terminal(mon), charging_index);

    v1_all(:,mon)=v1;
    x1_all(:,:,mon)=x1;
%     v2_all(:,mon)=v2;
%     x2_all(:,:,mon)=x2;

end

txt = sprintf('example.mat');
save(txt);





