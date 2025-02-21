import models as _models

############################################################


class Basis:
    """
    list of tuple where tuple possess the QN convention in models
    """

    def __init__(self, list_of_tuple):
        if len(list_of_tuple) == 0:
            self.list_of_qnums = _models.basis[_models.quantum_name]["zero"]
        else:
            self.list_of_qnums = sorted(set(list_of_tuple))

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return False
        return self.list_of_qnums == rhs.list_of_qnums

    def __str__(self):
        return "{0} : ".format(_models.quantum_name) + self.list_of_qnums.__str__()

    def __repr__(self):
        return self.__str__()

    def __add__(self, rhs):
        if isinstance(rhs, self.__class__):
            return Basis(
                sorted(
                    set(
                        [
                            _models.internal_sum_qn(qn1, qn2)
                            for qn1 in self.list_of_qnums
                            for qn2 in rhs.list_of_qnums
                        ]
                    )
                )
            )

    def __sub__(self, rhs):  # not commutative
        if isinstance(rhs, self.__class__):
            return Basis(
                sorted(
                    set(
                        [
                            _models.internal_sub_qn(qn1, qn2)
                            for qn1 in self.list_of_qnums
                            for qn2 in rhs.list_of_qnums
                        ]
                    )
                )
            )

    def intersection(self, other):
        if isinstance(other, self.__class__):
            return Basis(
                sorted(set(self.list_of_qnums).intersection(set(other.list_of_qnums)))
            )

    def __len__(self):
        return len(self.list_of_qnums)

    def __getitem__(self, pos):
        if 0 <= pos and pos < len(self):
            return self.list_of_qnums[pos]

    def which_type(self):
        return "B"

    # def filter(self):
    #     max_quantum_distances = [100]
    #     if _models.quantum_name=='sh-U1':
    #         if (len(self)<=max_quantum_distances[0]):
    #             return self
    #         else:
    #             index_distance = [(i,abs(conserved_quantum_numbers[0]-_)) for i,_ in enumerate(self.mz)]
    #             index_distance.sort(key=lambda x: x[1])
    #             distance = max_quantum_distances[0]
    #             if index_distance[distance-1][1]==index_distance[distance][1]:
    #                 distance += 1
    #             elem_index = [index_distance[i][0] for i in xrange(len(index_distance)) if (i<distance)]

    #             return Basis(*[self.mz[i] for i in xrange(len(self.mz)) if i in elem_index])
    #     if _models.quantum_name=='sh-SU2':
    #         return "TODO"
    #     if _models.quantum_name=='sh-None':
    #         return Basis(_models.basis[_models.quantum_name]['zero'])
    # def return_raw_basis(self):
    #     if quantum_name=='shU1':
    #         return self.mz
    #     if quantum_name=='shU2':
    #         pass


############################################################

# class Collection():
#     """
#     is a group of basis,Dummy,Collection
#     """
#     def __init__(self,*list_of_basis_depends_of_convention):
#         self.collection = list_of_basis_depends_of_convention
#     # def __eq__(self,rhs):
#     #     if not isinstance(rhs,self.__class__):
#     #         return False


############################################################


class Dummy:
    """
    No QN, only degeneracies! Not sensitive to global variables
    and QN conservation
    """

    def __init__(self, degeneracy):
        self.deg = degeneracy

    def __eq__(self, rhs):
        return self.deg == rhs.deg

    def __str__(self):
        return "Deg : {0}".format(self.deg)

    def __repr__(self):
        return self.__str__()

    def __add__(self, rhs):
        if isinstance(rhs, self.__class__):
            return self.deg + rhs.deg

    def __sub__(self, rhs):
        if isinstance(rhs, self.__class__):
            return self.deg + rhs.deg

    def __len__(self):
        return self.deg

    def __getitem__(self, pos):
        return pos

    def which_type(self):
        return "D"


############################################################

# class Family():
#     def __init__(self,*list_of_qnum_depends_of_convention):
#         if quantum_name in ['shU1', 'shU2']:
#             self.first = list_of_qnum_depends_of_convention[0]
#             self.last  = list_of_qnum_depends_of_convention[1]
#     def __eq__(self,rhs):
#         if not isinstance(rhs,self.__class__):
#             return False
#         if quantum_name=='shU1':
#             return ((self.first == rhs.first) and (self.last == rhs.last))
#     def __str__(self):
#         if quantum_name=='shU1':
#             return '(Fam|{0}..{1}>)'.format(self.first,self.last)
#     def __repr__(self):
#         return self.__str__()
#     def __add__(self,rhs):
#         # if isinstance(rhs,self.__class__):
#         #     return Family(self.first+rhs.first,self.last+rhs.last)
#         # else:
#         return [rhs]
#     def __len__(self):
#         return 1
#     def __getitem__(self,pos):
#         return self
#     def is_family(self):
#         return True
#     def which_type(self):
#         return 'F'


def basis_to_dict(basis):
    char_id = basis.which_type()
    dict_out = dict({})
    if char_id == "B":
        dict_out["qn_type"] = "B"
        dict_out["len"] = len(basis.list_of_qnums)
        # print('aie bas-dict')
        # # dict_out['bas'] = [list(_) for _ in basis.list_of_qnums]
        dict_out["bas"] = basis.list_of_qnums
        # dict_out['bas'] = _np.array(basis.list_of_qnums)
    if char_id == "D":
        dict_out["len"] = len(basis)
        dict_out["qn_type"] = "D"
    return dict_out


def dict_to_basis(dict_in, dummy=True):
    if dummy:
        return Dummy(dict_in["len"])
    else:
        char_id = dict_in["qn_type"]
        if char_id == "B":
            # return Basis([tuple(_) for _ in list(dict_in['bas'])])
            return Basis([tuple(_) for _ in dict_in["bas"]])
        if char_id == "D":
            return Dummy(dict_in["len"])


# def basis_of_dof():
#     if quantum_name=='shU1':
#         return Basis(*[-1,1])
#     if quantum_name=='shU2':
#         return Basis(*[(-1,-1),(1,1)])

# def left_family_at_site(i,L,mpo=True):
#     if i==1:
#         if quantum_name=='shU1':
#             return Basis(0)
#         if quantum_name=='shU2':
#             return Basis(*[(0,0)])
#     else:
#         if quantum_name=='shU1':
#             if mpo:
#                 return Family(-2*(i-1),2*(i-1))
#             else:
#                 return Family(-(i-1),(i-1))

# def right_family_at_site(i,L,mpo=True):
#     if i%L==0:
#         if quantum_name=='shU1':
#             return Basis(conserved_quantum_numbers[0])
#         if quantum_name=='shU2':
#             return Basis(*[(conserved_quantum_numbers[0],conserved_quantum_numbers[1])])
#     else:
#         if quantum_name=='shU1':
#             if mpo:
#                 return Family(-2*i,2*i)
#             else:
#                 return Family(-i,i)


def retained_QN_mixed(bas, keys, direction_right):
    if direction_right:
        left_generated = []
        for it in keys:
            left_generated.append(_models.internal_sum_qn(bas[0][it[0]], bas[1][it[1]]))
        return Basis(left_generated)
    else:
        right_generated = []
        for it in keys:
            right_generated.append(
                _models.internal_sum_qn(bas[3][it[3]], bas[2][it[2]])
            )
            # print('aie') ; right_generated.append(_models.internal_sub_qn(bas[3][it[3]],bas[2][it[2]]))
        return Basis(right_generated)


# def retained_QN(bas,keys, direction_right):
#     if direction_right:
#         left_generated  = []
#         for it in keys:
#             left_generated.append(_models.internal_sum_qn(bas[0][it[0]],bas[1][it[1]]))
#         return Basis(left_generated)
#     else:
#         right_generated = []
#         for it in keys:
#             right_generated.append(_models.internal_sub_qn(bas[3][it[3]],bas[2][it[2]]))
#         return Basis(right_generated)

# def retained_QN(bas,keys, direction_right):
#     # if direction_right:
#     #     left_generated  = []
#     #     for it in keys:
#     #         left_generated.append(_models.internal_sum_qn(bas[0][it[0]],bas[1][it[1]]))
#     #     return Basis(left_generated)
#     # else:
#     #     right_generated = []
#     #     for it in keys:
#     #         right_generated.append(_models.internal_sub_qn(bas[3][it[3]],bas[2][it[2]]))
#     #     return Basis(right_generated)
#     isLbasis = isinstance(bas[0],Basis)
#     isRbasis = isinstance(bas[-1],Basis)
#     left_generated  = []
#     right_generated = []
#     if isLbasis:
#         for it in keys:
#             left_generated.append(_models.internal_sum_qn(bas[0][it[0]],bas[1][it[1]]))
#     if isRbasis:
#         for it in keys:
#             right_generated.append(_models.internal_sub_qn(bas[2][it[2]],bas[3][it[3]]))
#     if len(left_generated)!=0 and len(right_generated)!=0:
#         return Basis(list(set(left_generated).intersection(set(right_generated))))
#         # return Basis(list(set(left_generated).union(set(right_generated)))).filter()
#     elif len(left_generated)!=0 and len(right_generated)==0:
#         return Basis(left_generated).filter()
#     elif len(left_generated)==0 and len(right_generated)!=0:
#         return Basis(right_generated).filter()
#     else:
#         print("error in retained_QN")


def degeneracy_in_QN_mixed(bas, keys, middle, direction_right):
    # print("IN degeneracy_in_QN, middle is :",middle)
    # isLbasis = isinstance(bas[0],Basis)
    # isRbasis = isinstance(bas[-1],Basis)

    nondeg = []
    degenerate = []
    # if isLbasis and not isRbasis: # bas[0]+bas[1]
    # print('len(middle)',len(middle))
    if direction_right:
        for j in xrange(len(middle)):
            # print('j=',j)
            tmp = []
            for it in keys:
                # print('middle[j]=',middle[j])
                # print('internal_sum_qn(bas[0][it[0]],bas[1][it[1]])=',internal_sum_qn(bas[0][it[0]],bas[1][it[1]]))
                if middle[j] == _models.internal_sum_qn(bas[0][it[0]], bas[1][it[1]]):
                    tmp.append(it)
            # print('tmp=',tmp)
            if len(tmp) > 1:
                degenerate.append((j, tmp))
            elif len(tmp) == 1:
                nondeg.append((j, tmp[0]))
    if not direction_right:
        for j in xrange(len(middle)):
            # print('j=',j)
            tmp = []
            for it in keys:
                # print('middle[j]=',middle[j])
                # print('internal_sum_qn(bas[0][it[0]],bas[1][it[1]])=',internal_sum_qn(bas[0][it[0]],bas[1][it[1]]))
                if middle[j] == _models.internal_sum_qn(bas[2][it[2]], bas[3][it[3]]):
                    tmp.append(it)
            # print('tmp=',tmp)
            if len(tmp) > 1:
                degenerate.append((j, tmp))
            elif len(tmp) == 1:
                nondeg.append((j, tmp[0]))
    # elif not isLbasis and isRbasis: # bas[2]+bas[3]
    #     for j in xrange(len(middle)):
    #         tmp = []
    #         for it in keys:
    #             if (bas[3][it[3]] == _models.internal_sum_qn(middle[j],bas[2][it[2]])):
    #                 tmp.append(it)
    #         if len(tmp) > 1:
    #             degenerate.append((j,tmp))
    #         elif len(tmp) == 1:
    #             nondeg.append((j,tmp[0]))
    # elif isLbasis and isRbasis: # else: # bas[0]+bas[1]  &&   bas[2]+bas[3]
    # for j in xrange(len(middle)):
    #     tmp = []
    #     # print('middle[j]=',middle[j])
    #     for it in keys:
    #         # print("DAMN it HOW MANY")
    #         # print('bas[0][it[0]]=',bas[0][it[0]])
    #         # print('bas[1][it[1]]=',bas[1][it[1]])
    #         # print('middle[j] == _models.internal_sum_qn(bas[0][it[0]],bas[1][it[1]])',middle[j] == _models.internal_sum_qn(bas[0][it[0]],bas[1][it[1]]))
    #         if (middle[j] == _models.internal_sum_qn(bas[0][it[0]],bas[1][it[1]]) and middle[j] == _models.internal_sub_qn(bas[2][it[2]],bas[3][it[3]]) ):
    #             tmp.append(it)
    #     # print('tmp=',tmp)
    #     if len(tmp) > 1:
    #         degenerate.append((j,tmp))
    #     elif len(tmp) == 1:
    #         nondeg.append((j,tmp[0]))
    # else:
    #     print("what should I do?!?!?!? SVD without QN")

    return nondeg, degenerate


# def basis_basic():
#     return basis[quantum_name]['qn']
# def basis_zero():
#     return basis[quantum_name]['zero']
