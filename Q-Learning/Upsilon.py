import math


def upsilon(x):
    P0 = 0.064 * 1e-3
    Pmax = 4.927 * 1e-3
    nu = 0.29
    tau = 274
    y = max(Pmax/math.exp(-tau * P0 + nu) * ((1 + math.exp(-tau * P0 + nu))/(1 + math.exp(-tau * x + nu)) - 1), 0); # See equation(4) in SectionII - Dof[2]
    return y
