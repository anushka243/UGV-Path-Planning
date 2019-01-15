function [K, M, states, charging_states, user_location_all, start, terminal] = environment(K, M, monte)
states=cell(M,1);
for m=1:M
    states{m}=2*[mod(m-1,sqrt(M)), floor((m-1)/(sqrt(M)))]; % 20m*20m square area
end
D=zeros(M,M); % distance between any two states
for m=1:M
    for j=1:M
        D(m,j) = norm(states{m}-states{j});
        if D(m,j)>1
            D(m,j)=1e6;
        end
    end
end

charging_states=cell(K,monte); % the charging regions for all the users
user_location_all=cell(monte);
rho=1e-3; % pathloss at 1 meter
Pt=1; % UGV transmit power, 1 Watt

for mon=1:monte
    % user location
    user_location=unifrnd(0,20,K,2);
    user_location_all{mon}=user_location;
    d=zeros(K,M); % distance between vertices and users
    for m=1:M
        for k=1:K
            d(k,m)=norm(states{m}-user_location(k,:));
        end
    end
    
    PL=zeros(K,M); % pathloss
    for m=1:M
        for k=1:K
            PL(k,m)=rho*(d(k,m)^(-2.5)); % pathloss
        end
    end
    % combine pathloss with fading
    for m=1:M
        for k=1:K
            g(k,m)=sqrt(PL(k,m))*sqrt(0.5)*(randn+sqrt(-1)*randn);
        end
    end  
    % compute the received power
    received_power=zeros(K,M); % received power at user k from vertex m
    for m=1:M
        for k=1:K
            received_power(k,m)=Pt.*g(k,m);
        end
    end
    % compute the harvested power   
    harvested_power=zeros(K,M); % harvested power at user k from vertex m
    for m=1:M
        for k=1:K
            harvested_power(k,m)=Upsilon(received_power(k,m));
        end
    end
    % compute the charging states
    charging_target=5*1e-3*rand(K,1); % 0~5 mW
    for m=1:M
        for k=1:K
            if harvested_power(k,m)>=charging_target(k)
                charging_states{k,mon}=[charging_states{k,mon}; states{m}];
            end
        end
    end       
end
start=[0,0];
terminal=[18,18];
end

