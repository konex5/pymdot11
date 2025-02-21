{ buildPythonPackage, fhmdot, nix-gitignore, numpy, pytestCheckHook, scipy }:

buildPythonPackage rec {
  pname = "pyfhmdot";
  version = "0.0";
  src = nix-gitignore.gitignoreSourcePure [ ".gitignore" "buil*" ] ./.;

  propagatedBuildInputs = [ fhmdot numpy ];

  checkInputs = [ pytestCheckHook scipy ];
  pytestFlagsArray = [ "tests" "-vv" ];
}
