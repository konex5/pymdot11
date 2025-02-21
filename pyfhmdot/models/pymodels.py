import numpy as _np
from scipy.linalg import expm as _expm

from pyfhmdot.models.pyoperators import single_operator, two_sites_bond_operator


def pyhamiltonian(name):
    models = {
        "skeleton": {
            "sub_model": "list_sub_ham_with_param",
            "on_site": "on_site_term",
            "nn_bond": "bond_term",
        },
        "sh_hx_no": {
            "sub_model": [],
            "on_site": [("hx", -1.0, "sh_sx_no")],
            "nn_bond": [],
        },
        "sh_hz_no": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "sh_sz_no")],
            "nn_bond": [],
        },
        "sh_hz_u1": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "sh_sz_u1")],
            "nn_bond": [],
        },
        "sh_xy_no": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [
                ("Jxy", 1.0 / 2.0, "sh_sp_no-sh_sm_no"),
                ("Jxy", 1.0 / 2.0, "sh_sm_no-sh_sp_no"),
            ],
        },
        "sh_xy_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [
                ("Jxy", 1.0 / 2.0, "sh_sp_u1-sh_sm_u1"),
                ("Jxy", 1.0 / 2.0, "sh_sm_u1-sh_sp_u1"),
            ],
        },
        "sh_zz_no": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jz", 1.0, "sh_sz_no-sh_sz_no")],
        },
        "sh_zz_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jz", 1.0, "sh_sz_u1-sh_sz_u1")],
        },
        "sh_xxz_no": {
            "sub_model": ["sh_xy_no", "sh_zz_no"],
            "on_site": [],
            "nn_bond": [],
        },
        "sh_xxz_u1": {
            "sub_model": ["sh_xy_u1", "sh_zz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "sh_xxz-hz_no": {
            "sub_model": ["sh_xxz_no", "sh_hz_no"],
            "on_site": [],
            "nn_bond": [],
        },
        "sh_xxz-hz_u1": {
            "sub_model": ["sh_xxz_u1", "sh_hz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
    }
    hamiltonian = {"on_site": [], "nn_bond": []}

    def append_sub_model(models, name, dst_hamiltonian):
        for sub_name in models[name]["sub_model"]:
            for on_site in models[sub_name]["on_site"]:
                dst_hamiltonian["on_site"].append(on_site)
            for bond in models[sub_name]["nn_bond"]:
                dst_hamiltonian["nn_bond"].append(bond)
            append_sub_model(models, sub_name, dst_hamiltonian)

    append_sub_model(models, name, hamiltonian)

    return hamiltonian


def on_site_operators_from_hamiltonian(name, parameters):
    hamiltonian = pyhamiltonian(name)

    single_operators = []
    for on_site in hamiltonian["on_site"]:
        single_operators.append(
            single_operator(name=on_site[-1], coef=parameters[on_site[0]] * on_site[1])
        )

    return single_operators


def nn_bond_operators_from_hamiltonian(name, parameters, *, weight_on_left=None):
    hamiltonian = pyhamiltonian(name)

    two_sites_bond_operators = []
    for nn_bond in hamiltonian["nn_bond"]:
        two_sites_bond_operators.append(
            two_sites_bond_operator(
                name=nn_bond[-1],
                coef=parameters[nn_bond[0]] * nn_bond[1],
                weight_on_left=weight_on_left,
            )
        )

    return two_sites_bond_operators


"""
    models = {
        # ### SKELETON
        "skeleton_model_name": {
            "nb_param": "list_param",
            "qn_name_allowed": "qn_name_allowed",
            "period": "ham_periodicity",
            "submodel": "list_of_submodel",
            "ham_expr": "expression_to_add__1-ONSITE__2-NEAREST_NEIGHBOR__3-SPECIAL-SITE__4-SPECIAL-BOND",
        },
        # ### sh-so CHAINS
        "hx": {
            "nb_param": 1,
            "qn_name_allowed": ["no"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("hx", -1.0, 0), ("sx", 0))], [], [], []],
        },
        "hz": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("hz", -1.0, 0), ("sz", 0))], [], [], []],
        },
        "xy": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxy", 1.0 / 2.0, 0), ("SpoSm", 0)),
                    (("Jxy", 1.0 / 2.0, 0), ("SmoSp", 0)),
                ],
                [],
                [],
            ],
        },
        "xydimer": {
            "nb_param": 2,
            "qn_name_allowed": ["no", "u1"],
            "period": 2,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxy_LIST", 1.0 / 2.0, 0), ("SpoSm", 0)),
                    (("Jxy_LIST", 1.0 / 2.0, 0), ("SmoSp", 0)),
                    (("Jxy_LIST", 1.0 / 2.0, 1), ("SpoSm", 1)),
                    (("Jxy_LIST", 1.0 / 2.0, 1), ("SmoSp", 1)),
                ],
                [],
                [],
            ],
        },
        "xyflux": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxy_EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpoSm", 0)),
                    (("Jxy_EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmoSp", 0)),
                ],
                [],
                [],
            ],
        },
        "zz": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[], [(("Jz", 1.0, 0), ("SzoSz", 0))], [], []],
        },
        "zzdimer": {
            "nb_param": 2,
            "qn_name_allowed": ["no", "u1"],
            "period": 2,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jz_LIST", 1.0, 0), ("SzoSz", 0)),
                    (("Jz_LIST", 1.0, 1), ("SzoSz", 1)),
                ],
                [],
                [],
            ],
        },
        "ionanisotropy": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("D", +1.0, 0), ("Sz^2", 0))], [], [], []],
        },
        "xxz": {
            "nb_param": 2,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [("xy", [0]), ("zz", [1])],
            "ham_expr": [[], [], [], []],
        },
        "xxz-hz": {
            "nb_param": 3,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [("xxz", [0, 1]), ("hz", [2])],
            "ham_expr": [[], [], [], []],
        },
        "xxx-dimer": {
            "nb_param": 2,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [("xydimer", [0, 1]), ("zzdimer", [0, 1])],
            "ham_expr": [[], [], [], []],
        },
        "xxx-dimer-hz": {
            "nb_param": 3,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [("xydimer", [0, 1]), ("zzdimer", [0, 1]), ("hz", [2])],
            "ham_expr": [[], [], [], []],
        },
         "xxz-SxBord": {
            "nb_param": 3,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [("xy", [0]), ("zz", [1]), ("SxRIGHT", [2]), ("SxLEFT", [2])],
            "ham_expr": [[], [], [], []],
        }, 
        # ### so spin ONE
        "xxz-Dz-hz": {
            "nb_param": 4,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [("xxz", [0, 1]), ("ionanisotropy", [2]), ("hz", [3])],
            "ham_expr": [[], [], [], []],
        },
        # ### ld LADDERS
        "ldhxId": {
            "nb_param": 1,
            "qn_name_allowed": ["no"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("hx", -1.0, 0), ("SxId", 0))], [], [], []],
        },
        "ldIdhx": {
            "nb_param": 1,
            "qn_name_allowed": ["no"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("hx", -1.0, 0), ("IdSx", 0))], [], [], []],
        },
        "ldhzId": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("hz", -1.0, 0), ("SzId", 0))], [], [], []],
        },
        "ldIdhz": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("hz", -1.0, 0), ("IdSz", 0))], [], [], []],
        },
        "ldxy-rung": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [
                    (("Jxyperp", 1.0 / 2.0, 0), ("SpSm", 0)),
                    (("Jxyperp", 1.0 / 2.0, 0), ("SmSp", 0)),
                ],
                [],
                [],
                [],
            ],
        },
        "ldxy-leg11": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxypara", 1.0 / 2.0, 0), ("SpIdoSmId", 0)),
                    (("Jxypara", 1.0 / 2.0, 0), ("SmIdoSpId", 0)),
                ],
                [],
                [],
            ],
        },
        "ldxy-leg22": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxypara", 1.0 / 2.0, 0), ("IdSpoIdSm", 0)),
                    (("Jxypara", 1.0 / 2.0, 0), ("IdSmoIdSp", 0)),
                ],
                [],
                [],
            ],
        },
        "ldxy-leg12": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxycross", 1.0 / 2.0, 0), ("SpIdoIdSm", 0)),
                    (("Jxycross", 1.0 / 2.0, 0), ("SmIdoIdSp", 0)),
                ],
                [],
                [],
            ],
        },
        "ldxy-leg21": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxycross", 1.0 / 2.0, 0), ("IdSpoSmId", 0)),
                    (("Jxycross", 1.0 / 2.0, 0), ("IdSmoSpId", 0)),
                ],
                [],
                [],
            ],
        },
        "ldxy-flux-rung": {
            "nb_param": 2,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [
                    (("Jxyperp_EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpSm", 0)),
                    (("Jxyperp_EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmSp", 0)),
                ],
                [],
                [],
                [],
            ],
        },
        "ldxy-flux-leg11": {
            "nb_param": 1,
            "qn_name_allowed": ["no", "u1"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("Jxypara_EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpIdoSmId", 0)),
                    (("Jxypara_EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmIdoSpId", 0)),
                ],
                [],
                [],
            ],
        },
        "ldxy-flux-leg22": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [],
            "ham_expr": [
                [],
                [
                    (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("IdSpoIdSm", 0)),
                    (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("IdSmoIdSp", 0)),
                ],
                [],
                [],
            ],
        },
        "ldxy-flux-border-rung": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": -1,
            "submodel": [],
            "ham_expr": [
                [],
                [],
                [
                    (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpSm", ("RIGHT", 0))),
                    (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmSp", ("RIGHT", 0))),
                    (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SpSm", ("LEFT", 0))),
                    (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SmSp", ("LEFT", 0))),
                ],
                [],
            ],
        },
        "ldzz-rung": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[(("M", 1.0, 0), ("SzSz", 0))], [], [], []],
        },
        "ldzz-leg11": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[], [(("M", 1.0, 0), ("SzIdoSzId", 0))], [], []],
        },
        "ldzz-leg22": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[], [(("M", 1.0, 0), ("IdSzoIdSz", 0))], [], []],
        },
        "ldzz-leg12": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[], [(("M", 1.0, 0), ("SzIdoIdSz", 0))], [], []],
        },
        "ldzz-leg21": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [],
            "ham_expr": [[], [(("M", 1.0, 0), ("IdSzoSzId", 0))], [], []],
        },
        # # 'ldzzL2sites' : {'nb_param' : 1, 'qname_ideal' : ['SU2detached', (2,)],'qname_allowed' : ['None','U1comb','SU2detached'], 'period' : 1,
        # #     'submodel' : [],
        # #     'ham_expr' : [ [], [( 0, ('M', [1.]), ('SzSz', 0) )], [], [] ] },
        # 'ldzzIdleg11dimer' : {'nb_param' : 2, 'qname_ideal' : ['SU2detached', (2,)],'qname_allowed' : ['None','U1comb','SU2detached'], 'period' : 2,
        #     'submodel' : [],
        #     'ham_expr' : [ [], [( 0, ('M', [1.]), ('SzIdoSzId', 0) ),( 1, ('M', [1.]), ('SzIdoSzId', 1) )], [], [] ] },
        # 'ldIdzzleg22dimer' : {'nb_param' : 2, 'qname_ideal' : ['SU2detached', (2,)],'qname_allowed' : ['None','U1comb','SU2detached'], 'period' : 2,
        #     'submodel' : [],
        #     'ham_expr' : [ [], [( 0, ('M', [1.]), ('IdSzoIdSz', 0) ),( 1, ('M', [1.]), ('IdSzoIdSz', 1) )], [], [] ] },
        "ldxxz-rung": {
            "nb_param": 2,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "SU2detached", "U1comb"],
            "period": 1,
            "submodel": [("ldxy-rung", [0]), ("ldzz-rung", [1])],
            "ham_expr": [[], [], [], []],
        },
        "ldxxz-legs": {
            "nb_param": 2,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "SU2detached", "U1comb"],
            "period": 1,
            "submodel": [
                ("ldxy-leg11", [0]),
                ("ldxy-leg22", [0]),
                ("ldzz-leg11", [1]),
                ("ldzz-leg22", [1]),
            ],
            "ham_expr": [[], [], [], []],
        },
        # model !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        "ldsnake0": {
            "nb_param": 2,
            "qname_ideal": ["U1comb", (1,)],
            "qname_allowed": ["None", "U1comb"],
            "period": 1,
            "submodel": [
                ("ldxy-rung", [0]),
                ("ldzz-rung", [0]),
                ("ldxy-leg12", [1]),
                ("ldzz-leg12", [1]),
            ],
            "ham_expr": [[], [], [], []],
        },
        "ldsnake1": {
            "nb_param": 2,
            "qname_ideal": ["U1comb", (1,)],
            "qname_allowed": ["None", "U1comb"],
            "period": 1,
            "submodel": [
                ("ldxy-rung", [0]),
                ("ldzz-rung", [0]),
                ("ldxy-leg21", [1]),
                ("ldzz-leg21", [1]),
            ],
            "ham_expr": [[], [], [], []],
        },
        # 'ldsnake0-dimer-hz' : {'nb_param' : 2, 'qname_ideal' : ['U1comb', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 1,
        #     'submodel' : [('ldxy-rung',[0]),('ldzz-rung',[0]),('ldhzId',[2]),('ldIdhz',[2])],
        #     'ham_expr' : [ [], [ ( 1, ('M', [1./2.]), ('SpIdoIdSm', 0)),(1, ('M', [1./2.]),('SmIdoIdSp', 0)),(1, ('M', [1.]),('SzIdoIdSz', 0)) ], [], [] ] },
        # 'ldsnake1-dimer-hz' : {'nb_param' : 2, 'qname_ideal' : ['U1comb', (2,)],'qname_allowed' : ['None','U1comb'], 'period' : 2,
        #     'submodel' : [('ldxy-rung',[0]),('ldzz-rung',[0]),('ldhzId',[2]),('ldIdhz',[2])],
        #     'ham_expr' : [ [], [ ( 1, ('M', [1./2.]), ('IdSpoIdSm', 0)),(1, ('M', [1./2.]),('IdSmoIdSp', 0)),(1, ('M', [1.]),('IdSzoIdSz', 0)),
        #                          ( 1, ('M', [1./2.]), ('SpIdoSmId', 1)),(1, ('M', [1./2.]),('SmIdoSpId', 1)),(1, ('M', [1.]),('SzIdoSzId', 1)) ], [], [] ] },
        "lr-xxz": {
            "nb_param": 4,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [("ldxxz-rung", [2, 3]), ("ldxxz-legs", [0, 1])],
            "ham_expr": [[], [], [], []],
        },
        "lr-xxz-hz": {
            "nb_param": 5,
            "qname_ideal": ["U1comb", (2,)],
            "qname_allowed": ["None", "U1comb"],
            "period": 1,
            "submodel": [("lr-xxz", [0, 1, 2, 3]), ("ldhzId", [4]), ("ldIdhz", [4])],
            "ham_expr": [[], [], [], []],
        },
        # 'ldxxz-hzN' : {'nb_param' : 3, 'qname_ideal' : ['None', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 1,
        #     'submodel' : [('ldxxz',[0,1]),('ldhzId',[2]),('ldIdhz',[2])],
        #     'ham_expr' : [ [], [], [], [] ] },
        # ###
        #
        #   /|\    /|\
        #  / | \  / | \
        # /__|  \/__|  \
        #
        "ldcoupled_triangle": {
            "nb_param": 5,
            "qname_ideal": ["U1comb", (1,)],
            "qname_allowed": ["None", "U1comb"],
            "period": 2,
            "submodel": [("ldhzId", [4])],
            "ham_expr": [
                [
                    (("M", 1.0 / 2.0, 0), ("SpSm", 1)),
                    (("M", 1.0 / 2.0, 0), ("SmSp", 1)),
                    (("M", 1.0, 1), ("SzSz", 1)),
                    (("M", -1.0, 4), ("IdSz", 1)),
                ],
                [
                    (("M", 1.0 / 2.0, 0), ("SpIdoSmId", 0)),
                    (("M", 1.0 / 2.0, 0), ("SmIdoSpId", 0)),
                    (("M", 1.0, 1), ("SzIdoSzId", 0)),
                    (("M", 1.0 / 2.0, 0), ("SpIdoIdSm", 0)),
                    (("M", 1.0 / 2.0, 0), ("SmIdoIdSp", 0)),
                    (("M", 1.0, 1), ("SzIdoIdSz", 1)),
                    (("M", 1.0 / 2.0, 2), ("IdSpoSmId", 1)),
                    (("M", 1.0 / 2.0, 2), ("IdSmoSpId", 1)),
                    (("M", 1.0, 3), ("IdSzoSzId", 1)),
                ],
                [],
                [],
            ],
        },
        # 'ldcoupled_triangle_flux' : {'nb_param' : 5, 'qname_ideal' : ['U1comb', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 2,
        #     'submodel' : [('ldhzId',[4])],
        #     'ham_expr' : [ [( ('M', 1./2., 0), ('SpSm', 1)), ( ('M', 1./2., 0), ('SmSp', 1)), ( ('M', 1., 1), ('SzSz', 1)), ( ('M', -1., 4), ('IdSz', 1)) ], [( ('M', 1./2., 0), ('SpIdoSmId', 0)),( ('M', 1./2., 0),('SmIdoSpId', 0)),( ('M', 1., 1),('SzIdoSzId', 0)), ( ('M', 1./2., 0), ('SpIdoIdSm', 0)), ( ('M', 1./2., 0),('SmIdoIdSp', 0)),( ('M', 1., 1),('SzIdoIdSz', 1)), ( ('M', 1./2., 2), ('IdSpoSmId', 1)),(('M', 1./2., 2),('IdSmoSpId', 1)),( ('M', 1., 3),('IdSzoSzId', 1)) ], [], [] ] },
        # 'ldcoupled_triangle_neel_flux' : {'nb_param' : 5, 'qname_ideal' : ['U1comb', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 4,
        #     'submodel' : [('ldhzId',[4])],
        #     'ham_expr' : [ [( ('M', 1./2., 0), ('SpSm', 1)), ( ('M', 1./2., 0), ('SmSp', 1)), ( ('M', 1., 1), ('SzSz', 1)), ( ('M', -1., 4), ('IdSz', 1)) ], [( ('M', 1./2., 0), ('SpIdoSmId', 0)),( ('M', 1./2., 0),('SmIdoSpId', 0)),( ('M', 1., 1),('SzIdoSzId', 0)), ( ('M', 1./2., 0), ('SpIdoIdSm', 0)), ( ('M', 1./2., 0),('SmIdoIdSp', 0)),( ('M', 1., 1),('SzIdoIdSz', 1)), ( ('M', 1./2., 2), ('IdSpoSmId', 1)),(('M', 1./2., 2),('IdSmoSpId', 1)),( ('M', 1., 3),('IdSzoSzId', 1)) ], [], [] ] },
        # 'ldcoupled_square' : {'nb_param' : 3, 'qname_ideal' : ['SU2', (2,)],'qname_allowed' : ['None','U1'], 'period' : 2,
        #     'submodel' : [('xyrung',[0]),('zzrung',[0]),('hzId',[2]),('Idhz',[2])],
        #     'ham_expr' : [ [ ], [( 0, ('M', [1./2.]), ('SpIdoSmId', 0)),(0, ('M', [1./2.]),('SmIdoSpId', 0)),(0, ('M', [1./2.]),('SzIdoSzId', 0)), ( 0, ('M', [1./2.]), ('IdSpoIdSm', 0)),(0, ('M', [1./2.]),('IdSmoIdSp', 0)),(0, ('M', [1./2.]),('IdSzoIdSz', 0)), ( 1, ('M', [1./2.]), ('SpIdoSmId', 1)),(1, ('M', [1./2.]),('SmIdoSpId', 1)),(1, ('M', [1./2.]),('SzIdoSzId', 1)), ( 1, ('M', [1./2.]), ('IdSpoIdSm', 1)),(1, ('M', [1./2.]),('IdSmoIdSp', 1)),(1, ('M', [1./2.]),('IdSzoIdSz', 1)) ], [], [] ] },
        "ldspincurrent": {
            "nb_param": 1,
            "qname_ideal": ["SU2detached", (2,)],
            "qname_allowed": ["None", "U1comb", "SU2detached"],
            "period": 1,
            "submodel": [
                ("ldxy-flux-leg11", [0]),
                ("ldxy-flux-leg22", [0]),
                ("ldxy-flux-border-rung", [0]),
            ],
            "ham_expr": [[], [], [], []],
        },
        # 'ldsh-xxx-hz-dimJ1J2' :
        #     {'nb_param' : 3, 'qname' : ['ldsh-U1comb', (2,)], 'period' : 2,
        #      'ham_expr' : [ [(1, 1/2.,'ldsh-SmIdIdSp'),(1, 1/2.,'ldsh-SpIdIdSm'),(1, 1/2.,'ldsh-IdSmSpId'),(1, 1/2.,'ldsh-IdSpSmId'),(1, 1.,'ldsh-SzIdIdSz'),(1, 1.,'ldsh-IdSzSzId')],
        #                     [(0, 1/2.,'ldsh-SpSm'),(0, 1/2.,'ldsh-SmSp'),(0, 1.,'ldsh-SzSz'),(2, -1.,'ldsh-SzId'),(2, -1.,'ldsh-IdSz')],
        #                     [],
        #                     [] ],
        #      'ham_expr0' : [ [(0, 1/2.,'ldsh-SmIdSpId'),(0, 1/2.,'ldsh-SpIdSmId'),(0, 1.,'ldsh-SzIdSzId')],
        #                     [],
        #                     [],
        #                     [] ],
        #      'ham_expr1' : [ [(0, 1/2.,'ldsh-IdSmIdSp'),(0, 1/2.,'ldsh-IdSpIdSm'),(0, 1.,'ldsh-IdSzIdSz')],
        #                     [],
        #                     [],
        #                     [] ]
        #  },
        # 'ldsh-xxz-hz-dimJ1J2' :
        #     {'nb_param' : 5, 'qname' : ['ldsh-U1comb', (2,)], 'period' : 2,
        #      'ham_expr' : [ [(2, 1/2.,'ldsh-SmIdIdSp'),(2, 1/2.,'ldsh-SpIdIdSm'),(2, 1/2.,'ldsh-IdSmSpId'),(2, 1/2.,'ldsh-IdSpSmId'),(3, 1.,'ldsh-SzIdIdSz'),(3, 1.,'ldsh-IdSzSzId')],
        #                     [(0, 1/2.,'ldsh-SpSm'),(0, 1/2.,'ldsh-SmSp'),(1, 1.,'ldsh-SzSz'),(4, -1.,'ldsh-SzId'),(4, -1.,'ldsh-IdSz')],
        #                     [],
        #                     [] ],
        #      'ham_expr0' : [ [(0, 1/2.,'ldsh-SmIdSpId'),(0, 1/2.,'ldsh-SpIdSmId'),(1, 1.,'ldsh-SzIdSzId')],
        #                     [],
        #                     [],
        #                     [] ],
        #      'ham_expr1' : [ [(0, 1/2.,'ldsh-IdSmIdSp'),(0, 1/2.,'ldsh-IdSpIdSm'),(1, 1.,'ldsh-IdSzIdSz')],
        #                     [],
        #                     [],
        #                     [] ]
        # }
    }
"""


def _mpo_from_operators(id_bloc, on_site, nn_bond_left, nn_bond_right):
    blocks = {}

    bl_dimL = len(nn_bond_left) + 1
    bl_dimR = len(nn_bond_right) + 1

    # id
    for idx, val in id_bloc.items():
        blocks[(0, idx[0], idx[1], 0)] = val.reshape(tuple([1] + list(val.shape) + [1]))
        blocks[(bl_dimL, idx[0], idx[1], bl_dimR)] = val.reshape(
            tuple([1] + list(val.shape) + [1])
        )
    # on_site
    for idx, val in on_site[0].items():
        blocks[(bl_dimL, idx[0], idx[1], 0)] = 0.5 * val.reshape(
            tuple([1] + list(val.shape) + [1])
        )  # appear twice in the bulk

    # nn_bond
    for i in range(1, bl_dimR, 1):
        for idxb, valb in nn_bond_right[i - 1].items():
            blocks[(i, idxb[0], idxb[1], 0)] = valb.reshape(
                tuple([1] + list(valb.shape) + [1])
            )

    for i in range(1, bl_dimL, 1):
        for idxa, vala in nn_bond_left[i - 1].items():
            blocks[(bl_dimL, idxa[0], idxa[1], i)] = vala.reshape(
                tuple([1] + list(vala.shape) + [1])
            )

    return blocks


def _mpo_from_operators_left_border(id_bloc, on_site, nn_bond_right):
    blocks = {}
    bl_dimR = len(nn_bond_right) + 1

    # id
    for idx, val in id_bloc.items():
        blocks[(0, idx[0], idx[1], bl_dimR)] = val.reshape(
            tuple([1] + list(val.shape) + [1])
        )

    # on site
    for idx, val in on_site[0].items():
        blocks[(0, idx[0], idx[1], 0)] = val.reshape(tuple([1] + list(val.shape) + [1]))

    # nn_bond
    for i in range(1, bl_dimR, 1):
        for idxa, vala in nn_bond_right[i - 1].items():
            blocks[(0, idxa[0], idxa[1], i)] = vala.reshape(
                tuple([1] + list(vala.shape) + [1])
            )

    return blocks


def _mpo_from_operators_right_border(id_bloc, on_site, nn_bond_left):
    blocks = {}
    bl_dimL = len(nn_bond_left) + 1

    # id
    for idx, val in id_bloc.items():
        blocks[(0, idx[0], idx[1], 0)] = val.reshape(tuple([1] + list(val.shape) + [1]))

    # on site
    for idx, val in on_site[0].items():
        blocks[(bl_dimL, idx[0], idx[1], 0)] = val.reshape(
            tuple([1] + list(val.shape) + [1])
        )

    # nn_bond
    for i in range(1, bl_dimL, 1):
        for idxb, valb in nn_bond_left[i - 1].items():
            blocks[(i, idxb[0], idxb[1], 0)] = valb.reshape(
                tuple([1] + list(valb.shape) + [1])
            )

    return blocks


def onsite_fuse_for_mpo(tmpblocks):
    difflab = list(set([tmp[0] for tmp in tmpblocks]))
    outblocks = []
    for lab in difflab:
        for l in range(len(tmpblocks)):
            if tmpblocks[l][0] == lab:
                shortlist = [_[0] for _ in outblocks]
                if lab not in shortlist:
                    outblocks.append(tmpblocks[l])
                else:
                    # can only be last # shortlist.index(lab)
                    outblocks[-1][1] += tmpblocks[l][1]
    return outblocks


def hamiltonian_obc(model_name, parameters, size):
    """
    qnmodel='sh_xxz-hz_no' or 'ru_ldxxz-hz_u1'
    """
    mpo = []
    head, _, tail = model_name.split("_")
    id_bloc = single_operator(name=head + "_id_" + tail, coef=1.0)
    on_site = on_site_operators_from_hamiltonian(model_name, parameters)
    # fuse on_site

    # fuse
    nn_bond = nn_bond_operators_from_hamiltonian(model_name, parameters)
    nn_bond_left = [_[0] for _ in nn_bond]
    nn_bond_right = [_[1] for _ in nn_bond]

    for site_i in range(size):
        if site_i == 0:
            mpo.append(_mpo_from_operators_left_border(id_bloc, on_site, nn_bond_right))
        elif site_i == size - 1:
            mpo.append(_mpo_from_operators_right_border(id_bloc, on_site, nn_bond_left))
        else:
            mpo.append(
                _mpo_from_operators(id_bloc, on_site, nn_bond_left, nn_bond_right)
            )
    return mpo


def _hamiltonian_gate_from_dense(id_bloc, on_site_left, on_site_right, nn_bond, *, d):

    if (
        _np.any([isinstance(x, complex) for x in on_site_left])
        or _np.any([isinstance(x, complex) for x in on_site_right])
        or _np.any([isinstance(x, complex) for x in nn_bond])
    ):
        t = _np.ndarray((d, d, d, d), dtype="complex128")
        t.fill(0)
    else:
        t = _np.ndarray((d, d, d, d))
        t.fill(0)

    # on_site_left
    t[:, :, :, :] += (_np.outer(on_site_left[0][(0, 0)], id_bloc[(0, 0)])).reshape(
        d, d, d, d
    )

    # on_site_right
    t[:, :, :, :] += (_np.outer(id_bloc[(0, 0)], on_site_right[0][(0, 0)])).reshape(
        d, d, d, d
    )

    # nn_bond
    for bond in nn_bond:
        t[:, :, :, :] += (_np.outer(bond[0][(0, 0)], bond[1][(0, 0)])).reshape(
            d, d, d, d
        )

    return t


def _exp_gate(arg, dH, *, d):
    #####
    # REMARK : exp(+arg dH) is before contracted with s..
    #  _|_|_  Wu,l Wu,l+1
    #  |___|
    #   | |   Wd,l Wd,l+1
    # ------- => exp(+arg dH)
    dU = _expm(+arg * (dH.transpose([0, 2, 1, 3])).reshape(d * d, d * d)).reshape(
        d, d, d, d
    )
    # dU.setflags(write=0)
    # [('Wd',(l+1)),('Wd',(l+2)),('Wu',(l+1)),('Wu',(l+2))])
    return dU


def _exp_dgate(arg, dH, *, d):
    # TMP correspond to exp(+arg dH)
    tmp = _exp_gate(arg, dH, d)
    #####
    # REMARK : exp(+arg dH) is before contracted with s..
    # ------- => dU = exp(+arg dH) et dU | ket >
    #  _|_|_  Wp,l Wp,l+1
    #  |_dU_|
    #   | |   sp,l sp,l+1
    # |||A||| => obs A     >
    #  _|_|_  sm,-l sm,-(l+1)
    #  |___|
    #   | |   Wm,-l Wm,-(l+1)
    # ------- => exp(+conj(arg) dH)

    # REMARK ABOUT TIME EVOLUTION WITH COMPLEX HAMILTONIAN !
    #
    # let's call dU = exp(-i dt dH)     (where arg=-i*dt for time)
    # of course dU^\dagger = exp(+i dt dH)
    #
    # so we have
    # A(t) = dU^\dagger A dU
    #
    # dU^\dagger = transpose(conj(dU))
    #
    # thus one should permute the label in the correct way after one
    # conjugate
    #
    # REMARK ENDED HERE !

    ###
    # # CORRECT BUT ALONE!
    # dU1 = _np.outer(tmp.reshape(d**4),_np.eye(d**2,d**2).reshape(d**4)).reshape(d,d,d,d,d,d,d,d)
    # dU1 = _np.outer(_np.eye(d**2,d**2).reshape(d**4),tmp.reshape(d**4)).reshape(d,d,d,d,d,d,d,d)
    # # CORRECT BUT ALONE!

    # dU2b = _np.outer(_np.conjugate(tmp).reshape(d**4),tmp.reshape(d**4)).reshape(d,d,d,d,d,d,d,d)
    # #dU2b=>[('s',-(l+1)),('s',-(l+2)),('W',-(l+1)),('W',-(l+2)),('W',+(l+1)),('W',+(l+2)),('s',+(l+1)),('s',+(l+2))]

    dU2 = _np.outer(_np.conjugate(tmp).reshape(d ** 4), tmp.reshape(d ** 4)).reshape(
        d, d, d, d, d, d, d, d
    )
    # dU2=>[('s',-(l+1)),('s',-(l+2)),('W',-(l+1)),('W',-(l+2)),('W',+(l+1)),('W',+(l+2)),('s',+(l+1)),('s',+(l+2))]
    # dU.setflags(write=0)
    return dU2


def _suzu_trotter_period2_exp_numpy(arg, site_L, site_R, bond_M, quantum_name, dgate):
    quantum_name_NONE = quantum_name.split("-")[0] + "-None"
    d = _models.basis[quantum_name_NONE]["deg"][0]

    dH = _gate_ham_period2_numpy(site_L, site_R, bond_M, quantum_name)
    if dgate == False:
        return _exp_gate(arg, dH, d)
    else:
        return _exp_dgate(arg, dH, d)


# below, cut from dense to quantum number (index + matrix)
def _generate_slices(d, deg):
    offi = 0
    for i in xrange(d):
        offj = 0
        for j in xrange(d):
            offk = 0
            for k in xrange(d):
                offl = 0
                for l in xrange(d):
                    yield i, j, k, l, slice(offi, (offi + deg[i])), slice(
                        offj, (offj + deg[j])
                    ), slice(offk, (offk + deg[k])), slice(offl, (offl + deg[l]))
                    offl += deg[l]
                offk += deg[k]
            offj += deg[j]
        offi += deg[i]


def _generate_slices_dgate(d, deg):
    offi = 0
    for i in xrange(d):
        offj = 0
        for j in xrange(d):
            offk = 0
            for k in xrange(d):
                offl = 0
                for l in xrange(d):
                    offm = 0
                    for m in xrange(d):
                        offn = 0
                        for n in xrange(d):
                            offo = 0
                            for o in xrange(d):
                                offp = 0
                                for p in xrange(d):
                                    yield i, j, k, l, m, n, o, p, slice(
                                        offi, (offi + deg[i])
                                    ), slice(offj, (offj + deg[j])), slice(
                                        offk, (offk + deg[k])
                                    ), slice(
                                        offl, (offl + deg[l])
                                    ), slice(
                                        offm, (offm + deg[m])
                                    ), slice(
                                        offn, (offn + deg[n])
                                    ), slice(
                                        offo, (offo + deg[o])
                                    ), slice(
                                        offp, (offp + deg[p])
                                    )
                                    offp += deg[p]
                                offo += deg[o]
                            offn += deg[n]
                        offm += deg[m]
                    offl += deg[l]
                offk += deg[k]
            offj += deg[j]
        offi += deg[i]


# above, cut from dense to quantum number (index + matrix)

############################################################
############################################################
############################################################


def suzu_trotter_period2_exp(arg, site_L, site_R, bond_M, quantum_name, dgate):
    # for gate : GOES OUT IN SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2))])
    #
    # for dgate : GOES OUT IN SSWW-SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2)),('W',-(l+1)),('W',-(l+2)),('s',-(l+1)),('s',-(l+2))])
    #
    deg = _models.basis[quantum_name]["deg"]
    d = len(deg)
    t = _suzu_trotter_period2_exp_numpy(
        arg, site_L, site_R, bond_M, quantum_name, dgate
    )

    blocks = []
    if dgate == False:
        for i, j, k, l, si, sj, sk, sl in _generate_slices(d, deg):
            tmp = t[si, sj, sk, sl]
            if not _np.all(tmp == 0):
                tmp.setflags(write=0)
                blocks.append([[i, j, k, l], tmp])
    else:
        for (
            i,
            j,
            k,
            l,
            m,
            n,
            o,
            p,
            si,
            sj,
            sk,
            sl,
            sm,
            sn,
            so,
            sp,
        ) in _generate_slices_dgate(d, deg):
            tmp = t[si, sj, sk, sl, sm, sn, so, sp]
            if not _np.all(tmp == 0):
                tmp.setflags(write=0)
                blocks.append([[i, j, k, l, m, n, o, p], tmp])
    return blocks


############################################################


def suzu_trotter_obc_exp(arg, qnmodel, param, L, dgate):
    # for gate : GOES OUT IN SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2))])
    #
    # for dgate : GOES OUT IN SSWW-SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2)),('W',-(l+1)),('W',-(l+2)),('s',-(l+1)),('s',-(l+2))])
    #
    qname = qnmodel.split("-")[0]
    # if qname[0:2]=='ld':
    #     model = 'ld-'+qnmodel.split(qname+'-')[-1]
    # else:
    #     model = qnmodel.split(qname+'-')[-1]

    quantum_name = (
        qname
        + "-"
        + _models.hamiltonian[qnmodel.split(qname + "-")[-1]]["qname_ideal"][0]
    )

    mpo = []
    onsite, onbond = finite_hamiltonian_terms(qnmodel, param, L)

    for l in xrange(L - 1):
        if l == 0:
            effectif_onsite_L = onsite[l]
        else:
            effectif_onsite_L = [(param / 2.0, name) for param, name in onsite[l]]

        if l == L - 2:
            effectif_onsite_R = onsite[L - 1]
        else:
            effectif_onsite_R = [(param / 2.0, name) for param, name in onsite[l + 1]]

        effectif_onbond = onbond[l]
        mpo.append(
            suzu_trotter_period2_exp(
                arg,
                effectif_onsite_L,
                effectif_onsite_R,
                effectif_onbond,
                quantum_name,
                dgate,
            )
        )

    return mpo


############################################################
# MATRICES ARE CORRECT!
# manybody.models.quantum_name = 'sh-None'
# A = manybody.matrices.suzu_trotter_obc_exp(-0.02,'sh-xxz-hz',[1,1,2],10,True)[0]
# manybody.models.quantum_name = 'sh-U1'
# B = manybody.matrices.suzu_trotter_obc_exp(-0.02,'sh-xxz-hz',[1,1,2],10,True)[0]
# for i in xrange(len(B)):
#     print(B[i][1][0,0,0,0] == A[0][1][tuple(B[i][0])])
