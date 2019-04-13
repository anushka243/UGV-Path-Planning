function [E_total, v, x] = shortestpath(K, M, g, D, terminal, charge)
alpha=[0.29, 7.4];
a=2; % 2m/s
receive=G_inv(charge);
power=zeros(M,1);
for m=1:M
    temp=0;
    for k=1:K
        temp=max(temp,receive./norm(g(k,m))^2);
    end
    power(m)=temp;
end

% solve the TSP using Gurobi
cvx_begin quiet
cvx_solver Mosek
% original variables
variable v(M) binary
variable x(M,M) binary

minimize trace(transpose(D)*x) % total path length
subject to

% divergence constraint
sum(x(1,:))==1;
sum(x(:,1))==0;
sum(x(terminal,:))==0;
sum(x(:,terminal))==1;
for m=2:M
    if m~=terminal
    sum(x(m,:))==v(m);
    sum(x(:,m))==v(m);
    end
end
for m=1:M
    x(m,m)==0;
end
v(1)==1;
v(terminal)==1;

cvx_end


E_total=trace(transpose(D)*x)./a*(alpha(1)+alpha(2)*a)+sum(v.*power);


