{ pkgs ? import
    (
      builtins.fetchTarball {
        url = "https://github.com/NixOS/nixpkgs/archive/902d91def1efbea804f5158e5999cb113cedf04b.tar.gz";
        sha256 = "sha256:1ya19ix77k2yn1c2gyzz644576c2qn11llrqhyy0c7a3y4dlwnn9";
      }
    )
    { }
}:

with pkgs;
assert hostPlatform.isx86_64;

let
  pythonEnv = python3.withPackages (ps: with ps; [
    #------------#
    # pydevtools #
    #------------#
    black
    flake8
    ipython
    mypy
    pylint
    pip
    # pygls
    # pyls-black
    # pyls-mypy
    pytest
    yapf
    #---------------#
    # documentation #
    #---------------#
    jupyter-sphinx
    sphinx
    sphinx_rtd_theme
    # nbformat
    # nbconvert
  ] ++ lib.optionals (!isPy39) [ python-language-server ]);
in
mkShell {
  propagatedBuildInputs = [ ];
  nativeBuildInputs = [ bashCompletion bashInteractive pythonEnv ];
  buildInputs = [ ] ++ lib.optionals (hostPlatform.isLinux) [ glibcLocales ];

  LANG = "en_US.UTF-8";

  shellHook = ''
    mkdir -p $(pwd)/.trash_config/
    export HOME=$(pwd)/.trash_config
    export PYTHONPATH=$PWD:$PYTHONPATH
    export SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt
  '';
}
