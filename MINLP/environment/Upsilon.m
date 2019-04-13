function y = Upsilon(x)
P0=0.064*1e-3;
Pmax=4.927*1e-3;
nu=0.29;
tau=274;

F=@(x) max(Pmax./exp(-tau*P0+nu)*((1+exp(-tau*P0+nu))./(1+exp(-tau*x+nu))-1),0); % See equation (4) in Section II-D of [2]
y=F(x);    
end

