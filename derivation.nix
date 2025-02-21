{ buildPythonPackage, fhmdot, numpy, pytestCheckHook, scipy, src }:

buildPythonPackage rec {
  pname = "pyfhmdot";
  version = "0.0";
  inherit src;

  propagatedBuildInputs = [ fhmdot numpy ];

  checkInputs = [ pytestCheckHook scipy ];
  pytestFlagsArray = [ "tests" "-vv" ];
}
