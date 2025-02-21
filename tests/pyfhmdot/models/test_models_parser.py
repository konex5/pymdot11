import pytest

@pytest.mark.skip
def test_hamiltonian_read_line():
    from pyfhmdot.models.parser import read_parameters

    name, value = read_parameters("Jz=2.57")
    assert name == "Jz" and value == 2.57
    name, value = read_parameters("J_EXP=2,1")
    assert name == "J_EXP" and value == (2, 1)
    name, value = read_parameters("J_LIST=2,1,5,6")
    assert name == "J_LIST" and isinstance(value, list) and value[-1] == 6


def test_read_write_params(tmpdir):
    params = {
        "xy": {"a": 1, "b_EXP": (2, 3), "c_LIST": [1, 2, 3, 4, 5, 6]},
        "zz": {"Jz": 1},
    }
    tmp_toml = tmpdir + "/test.toml"
    tmp_json = tmpdir + "/test.json"
    from pyfhmdot.models.parser import write_filename, read_filename

    write_filename(tmp_toml, params)
    write_filename(tmp_json, params)
    params_toml = read_filename(tmp_toml)
    params_json = read_filename(tmp_json)
    assert params_toml["xy"]["c_LIST"][-1] == 6
    assert params_json["xy"]["c_LIST"][-1] == 6
