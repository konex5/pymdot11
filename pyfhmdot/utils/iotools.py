import h5py as _h5


def check_instance(filepath):
    if not _h5.is_hdf5(filepath):
        raise Exception(f" <HDF5> {filepath} is not a valid h5 file")
    f = _h5.File(filepath, "r")
    if not "/QMP" in f:
        raise Exception(" <HDF5> MP is not a valid group in h5 file")
    if not "/QMP/0001" in f:
        raise Exception(" <HDF5> MP is void")
    f.close()


def add_dictionary(filepath, folder="INFO", dictionary={}):
    f = _h5.File(filepath, "r+")
    grp = f.create_group(folder)
    for k, v in dictionary.items():
        grp.create_dataset(k, data=v)
    f.close()


def load_dictionary(filepath, folder="MODEL"):
    f = _h5.File(filepath, "r")
    grp = f[folder]
    dictionary = dict()
    for key in grp.keys():
        dictionary[key] = grp[key].value
    f.close()
    return dictionary


def write_save_mp(filepath, MP):
    f = _h5.File(filepath, "w")
    # f.create_dataset('CHI',data=float('inf'))
    grpMP = f.create_group("MP")
    for i in range(len(MP)):
        grpMP.create_dataset(
            "{0:04g}".format(i + 1), data=MP[i], compression="gzip", compression_opts=9
        )
    f.close()


def load_generator_mp(filepath):
    f = _h5.File(filepath, "r")
    for m in f["/MP"].values():
        yield m.value
    f.close()


def writeIn_QMP_dict(QMP_dict, file_path, name="QMP", site=0):
    if not _h5.is_hdf5(file_path):
        raise Exception(
            " <HDF5> {file} is not a valid hdf5 file".format(file=file_path)
        )
    f = _h5.File(file_path, "r+")
    grp = f.create_group(name + "/{0:04g}".format(site))
    for it, val in QMP_dict.items():
        grp.create_dataset(
            "".join(["{0:02g}".format(_) for _ in it]),
            data=val,
            compression="gzip",
            compression_opts=9,
        )
    f.close()


def readIn_generator_QMP(file_path, rootname="QMP", coefsite=False, conjugate=False):
    if not _h5.is_hdf5(file_path):
        raise Exception(
            " <HDF5> {file} is not a valid hdf5 file".format(file=file_path)
        )
    f = _h5.File(file_path, "r")
    if coefsite:
        coefonsite_gen = (_ for _ in f["/" + rootname + "_coefsite"].value)
    for per_site in f["/" + rootname].values():
        block_array = dict()
        if coefsite:
            coefonsite = coefonsite_gen.next()
        for m in per_site.values():
            line = m.name.split("/")[-1]
            if coefsite and conjugate:
                block_array[
                    tuple(int(line[_ : (_ + 2)]) for _ in range(0, len(line), 2))
                ] = (coefonsite * m.value.conjugate())
            elif coefsite and not conjugate:
                block_array[
                    tuple(int(line[_ : (_ + 2)]) for _ in range(0, len(line), 2))
                ] = (coefonsite * m.value)
            elif not coefsite and conjugate:
                block_array[
                    tuple(int(line[_ : (_ + 2)]) for _ in range(0, len(line), 2))
                ] = m.value.conjugate()
            else:
                block_array[
                    tuple(int(line[_ : (_ + 2)]) for _ in range(0, len(line), 2))
                ] = m.value
        yield block_array
    f.close()
