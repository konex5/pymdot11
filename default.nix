{ pkgs ? import
    (
      builtins.fetchTarball {
        url = "https://github.com/NixOS/nixpkgs/archive/63dacb46bf939521bdc93981b4cbb7ecb58427a0.tar.gz";
        sha256 = "sha256:1lr1h35prqkd1mkmzriwlpvxcb34kmhc9dnr48gkm8hh089hifmx";
      }
    )
    { }
, clangSupport ? true
}:

with pkgs;

let

  pythonPackageOverrides = python-self: python-super: rec {
    fhmdot = python-self.callPackage ../fhmdot/derivation.nix {
      stdenv = if clangSupport then clangStdenv else gccStdenv;
      mdot = callPackage ../mdot/derivation.nix {
        stdenv = if clangSupport then clangStdenv else gccStdenv;
      };

    };
    pyfhmdot = python-self.callPackage ./derivation.nix {
      fhmdot = python-self.fhmdot;
    };

  };

  python = python3.override (old: {
    packageOverrides = lib.composeExtensions (old.packageOverrides or (_: _: { }))
      pythonPackageOverrides;
  });

  pythonPackages = python.pkgs;

in
{ inherit pythonPackages; }


