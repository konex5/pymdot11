{ pkgs ? import
    (
      builtins.fetchTarball {
        url = "https://github.com/NixOS/nixpkgs/archive/c00959877fb06b09468562518b408acda886c79e.tar.gz";
        sha256 = "sha256:02anj9mbzy45bszlmv7k42mb5y7yj2lxc5vpbxgd3f5qljn5ih7y";
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
