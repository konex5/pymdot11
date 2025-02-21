import h5py as _h5
import os


def create_h5(filepath):
    if os.path.exists(os.path.dirname(filepath)):
        with _h5.File(filepath, "w") as _:
            pass


def check_instance_mp(filepath):
    if not _h5.is_hdf5(filepath):
        raise Exception(f" <HDF5> {filepath} is not a valid h5 file")
    with _h5.File(filepath, "r") as f:
        if not "/QMP" in f:
            raise Exception(" <HDF5> MP is not a valid group in h5 file")
        if not "/QMP/0001" in f:
            raise Exception(" <HDF5> MP is void")


def add_dictionary(filepath, folder="INFO", dictionary={}):
    with _h5.File(filepath, "r+") as f:
        grp = f.create_group(folder)
        for k, v in dictionary.items():
            grp.create_dataset(k, data=v)


def load_dictionary(filepath, dictionary, folder="MODEL"):
    with _h5.File(filepath, "r") as f:
        grp = f[folder]
        for key in grp.keys():
            dictionary[key] = grp[key][()]


def write_single_mp(file_path, mp_dictionary, site=0, folder="QMP"):
    with _h5.File(file_path, "r+") as f:
        grp = f.create_group(f"/{folder}/{site:04g}")
        for it, val in mp_dictionary.items():
            grp.create_dataset(
                "".join(["{0:02g}".format(_) for _ in it]),
                data=val,
                compression="gzip",
                compression_opts=9,
            )


def load_single_mp(file_path, mp_dictionary, site=0, folder="QMP"):
    mp_dictionary.clear()
    with _h5.File(file_path, "r") as f:
        for m in f[f"/{folder}/{site:04g}"].values():
            line = m.name.split("/")[-1]
            mp_dictionary[
                tuple(int(line[_ : (_ + 2)]) for _ in range(0, len(line), 2))
            ] = m[()]
