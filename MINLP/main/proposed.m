%lowerbound
function [E_total, v, x] = proposed(K, M, D, terminal, charge)
alpha=[0.29, 7.4]; % tone coz we consider constant acceleration pioneer's 3DX robot experimental result
a=2; % 2m/s
R=length(charge);
X=zeros(M,M);
for m=1:M
    for j=1:M
        if D(m,j)>2.5 % distance between any two states is set as 2 and therefore more than that then UGv cant go
            X(m,j)=1;
        end
    end
end

% solve the MILP using Mosek
cvx_begin quiet
cvx_solver Mosek
% original variables
variable v(M) binary % visit a state or not
variable x(M,M) binary % matrix whetehr link between i to j

minimize trace(transpose(D)*x)./a*(alpha(1)+alpha(2)*a) % total motion power
subject to

x(X==1)==0; % if states are not neighbpours then links are not possible
% divergence constraint
sum(x(1,:))==1; % has to be link from outside and no link inside
sum(x(:,1))==0;
sum(x(terminal,:))==0;% vice versa
sum(x(:,terminal))==1;
for m=1:M
    if m~=terminal && m~=1
        sum(x(m,:))==v(m);
        sum(x(:,m))==v(m);
    end
end
for m=1:M
    x(m,m)==0;% it cannot go from onr point to the same point without any movement
end
v(1)==1;
v(terminal)==1;
for r=1:R
    sum(v(charge{r})) >=1;% have to change this as specifies all users
end


cvx_end
% %%
% M_lb=sum(v)-1;
% M_up=M-1;
% 
% for C=M_lb:M_up
%     J=1e6;
%     % solve the MILP using Mosek
%     cvx_begin
%     cvx_solver Mosek
%     % original variables
%     variable v(M) binary
%     variable x(M,M) binary
%     variable u(M)
%     
%     minimize trace(transpose(D)*x)./a*(alpha(1)+alpha(2)*a) % total motion power
%     subject to
%     
%     x(X==1)==0;
%     sum(x(1,:))==1;
%     sum(x(:,1))==0;
%     sum(x(terminal,:))==0;
%     sum(x(:,terminal))==1;
%     for m=1:M
%         if m~=terminal && m~=1
%             sum(x(m,:))==v(m);
%             sum(x(:,m))==v(m);
%         end
%     end
%     for m=1:M
%         x(m,m)==0;
%     end
%     v(1)==1;
%     
%     for r=1:R
%         sum(v(charge{r}))>=1;
%     end
%     
%     sum(v)==C+1;
%     % subtour elimination constraint
%     for m=2:M
%         if m~=terminal
%             for j=2:M
%                 if j~=terminal
%                     if m~=j
%                         u(m)-u(j)+(C-1)*x(m,j)+(C-3)*x(j,m)<=C-2+J*(2-v(m)-v(j));
%                     end
%                 end
%             end
%         end
%     end
%     
%     for m=1:M
%             u(m)>=v(m);
%             u(m)<=C-1;
%             u(m)<=J*v(m);
%     end
%     cvx_end
% 
%     if ~isnan(x)
%         E_total=trace(transpose(D)*x)./a*(alpha(1)+alpha(2)*a);  
%     disp(E_total);
%     break;
%     end
% end 

E_total=trace(transpose(D)*x)./a*(alpha(1)+alpha(2)*a);
end






