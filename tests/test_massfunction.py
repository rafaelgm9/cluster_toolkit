import pytest
import numpy as np
from cluster_toolkit import massfunction as mf
from cluster_toolkit import peak_height as peaks
import numpy.testing as npt
from os.path import dirname, join

h = 0.7 #arbitrary
Omega_m = 0.3 #arbitrary
datapath = "./data_for_testing/"
k = np.loadtxt(join(dirname(__file__),datapath+"klin.txt")) #h/Mpc; wavenumber
p = np.loadtxt(join(dirname(__file__),datapath+"plin.txt")) #[Mpc/h]^3 linear power spectrum

M = np.logspace(12, 16, num=20)

def test_dndM():
    n = mf.dndM_at_M(M, k/h, p, Omega_m)*M
    k2 = k/h
    n2 = np.array([mf.dndM_at_M(Mi, k2, p, Omega_m) for Mi in M])*M
    npt.assert_array_equal(n, n2)

def test_dndM_M():
    n = mf.dndM_at_M(M, k/h, p, Omega_m)*M
    npt.assert_array_less(n[1:], n[:-1])

    """
    #Can't run this test since we can't let the test depend on having class
    def test_dndM_z():
    #In the high mass end high z is always steeper
    Mz = np.logspace(14, 16, num=10) 
    nz0 = mf.dndM_at_M(Mz, k/h, p, Omega_m)*Mz
    z=1.
    p1 = np.array([cosmo.pk_lin(ki, z) for ki in k])*h**3 #Mpc^3/h^3
    nz1 = mf.dndM_at_M(Mz, k/h, p1, Omega_m)*Mz
    npt.assert_array_less(nz1, nz0)
    """

def test_G():
    sigma = np.sqrt(peaks.sigma2_at_M(M, k, p, Omega_m))
    Gm = mf.G_at_M(M, k, p, Omega_m)
    Gs = mf.G_at_sigma(sigma)
    R = Gm/Gs
    ones = np.ones_like(R)
    npt.assert_array_equal(ones, R)

def test_mf_binned():
    M2 = np.logspace(12, 16, num=100)
    dn = mf.dndM_at_M(M2, k/h, p, Omega_m)
    edges = np.logspace(12, 16, 11)
    n = mf.n_in_bins(edges, M2, dn)
    npt.assert_array_less(n[1:], n[:-1])
    n2 = np.array([mf.n_in_bin(edges[i], edges[i+1], M2, dn) for i in range(len(edges)-1)])
    npt.assert_array_less(n2[1:], n2[:-1])
    npt.assert_array_equal(n, n2)

def test_special():
    sigma2 = peaks.sigma2_at_M(M, k, p, Omega_m)
    Mt = M*(1-1e-6*0.5)
    Mb = M*(1+1e-6*0.5)
    sigma2t = peaks.sigma2_at_M(Mt, k, p, Omega_m)
    sigma2b = peaks.sigma2_at_M(Mb, k, p, Omega_m)
    d,e,f,g = 2.16087369917, 1.18309392312, 0.133881834517, -0.0263615354323
    n = mf._dndM_sigma2_precomputed(M, sigma2, sigma2t, sigma2b, Omega_m,d,e,f,g)
    npt.assert_array_less(n[1:], n[:-1])

    
if __name__=="__main__":
    test_dndM()
    test_dndM_M()
    test_mf_binned()
    test_G()
    test_special()
