import pytest


# @pytest.mark.skip("this test is a visual test with print")
def test_eleven_times(
    make_maximal_entangled_state_u1,
    make_single_dummy_dgate,
):
    from pyfhmdot.algorithm import sweep_eleven_times, sweep_eleven_times_hard

    # L=6; start_odd_bonds=True; start_left=True # ok for even and odd sites
    # sweep_eleven_times(L,L*[None], [(L-1)*[None],(L-1)*[None],(L-1)*[None],(L-1)*[None]],{"dw_one_serie":0, "dw_total": 0},10,True,10**-8,start_left=start_left,start_odd_bonds=start_odd_bonds)
    # L=6; start_odd_bonds=True; start_left=False # ok for even and odd_sites
    # sweep_eleven_times(L,L*[None], [(L-1)*[None],(L-1)*[None],(L-1)*[None],(L-1)*[None]],{"dw_one_serie":0, "dw_total": 0},10,True,10**-8,start_left=start_left,start_odd_bonds=start_odd_bonds)
    # L=6; start_odd_bonds=False; start_left=True # ok for even and odd sites
    # sweep_eleven_times(L,L*[None], [(L-1)*[None],(L-1)*[None],(L-1)*[None],(L-1)*[None]],{"dw_one_serie":0, "dw_total": 0},10,True,10**-8,start_left=start_left,start_odd_bonds=start_odd_bonds)
    L = 5
    start_odd_bonds = False
    start_left = False  # ok for even and odd sites
    # sweep_eleven_times(L,L*[None], [(L-1)*[None],(L-1)*[None],(L-1)*[None],(L-1)*[None]],{"dw_one_serie":0, "dw_total": 0},10,True,10**-8,start_left=start_left,start_odd_bonds=start_odd_bonds)

    ## real test
    dmps = make_maximal_entangled_state_u1(L=11)
    mpo = make_single_dummy_dgate()
    ggate = [11 * [mpo], 11 * [mpo], 11 * [mpo], 11 * [mpo]]
    sweep_eleven_times(
        dmps,
        ggate,
        {"dw_one_serie": 0, "dw_total": 0},
        5,
        True,
        10 ** -18,
        start_left=False,
        start_odd_bonds=start_odd_bonds,
    )
    pass
