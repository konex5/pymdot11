{ buildPythonPackage, fhmdot, src, click, decorator, jinja2, pyjson5, pytestCheckHook, toml }:

buildPythonPackage rec {
  pname = "pyfhmdot";
  version = "0.0";
  inherit src;

  propagatedBuildInputs = [ click decorator fhmdot jinja2 pyjson5 toml ];

  checkInputs = [ pytestCheckHook ];
  pytestFlagsArray = [ "tests" "-vv" ];
}
