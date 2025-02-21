{ pkgs ? import
    (
      builtins.fetchTarball {
        url = "https://github.com/NixOS/nixpkgs/archive/63dacb46bf939521bdc93981b4cbb7ecb58427a0.tar.gz";
        sha256 = "sha256:1lr1h35prqkd1mkmzriwlpvxcb34kmhc9dnr48gkm8hh089hifmx";
      }
    )
    { }
}:

with pkgs;
assert hostPlatform.isx86_64;

let
  pythonEnv = python3.withPackages (ps: with ps; [
    h5py
    matplotlib
    numpy
    scipy
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
    python-lsp-server
    #---------------#
    # documentation #
    #---------------#
    # jupyter-sphinx
    # sphinx
    # sphinx_rtd_theme
    # nbformat
    # nbconvert
  ]);
in
mkShell {
  propagatedBuildInputs = [ ];
  nativeBuildInputs = [ pythonEnv ];
  buildInputs = [ ] ++ lib.optionals (hostPlatform.isLinux) [ glibcLocales ];

  LANG = "en_US.UTF-8";

  shellHook = ''
    mkdir -p $(pwd)/.trash_config/
    export HOME=$(pwd)/.trash_config
    export PYTHONPATH=$PWD:$PYTHONPATH
    export SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt
  '';
}
