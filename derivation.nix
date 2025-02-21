{ buildPythonPackage
, mdot11
, numpy
, pytestCheckHook
, scipy
, src ? "./."
, version ? "0.1"
}:

buildPythonPackage rec {
  pname = "pyfhmdot";
  inherit version;
  inherit src;

  propagatedBuildInputs = [ mdot11 numpy ];

  checkInputs = [ pytestCheckHook scipy ];
  pytestFlagsArray = [ "tests" "-vv" ];
}
