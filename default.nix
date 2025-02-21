{ pkgs ? import
    (
      builtins.fetchTarball {
        url = "https://github.com/NixOS/nixpkgs/archive/902d91def1efbea804f5158e5999cb113cedf04b.tar.gz";
        sha256 = "sha256:1ya19ix77k2yn1c2gyzz644576c2qn11llrqhyy0c7a3y4dlwnn9";
      }
    )
    { }
, clangSupport ? true
}:

with pkgs;

let

  pythonPackageOverrides = python-self: python-super: rec {
    fhmdot = python-self.callPackage ../fhmdot/derivation.nix {
      src = ../fhmdot/.;
      stdenv = if clangSupport then clangStdenv else gccStdenv;
      mdot = callPackage ../mdot/derivation.nix {
        src = ../mdot/.;
        stdenv = if clangSupport then clangStdenv else gccStdenv;
      };

    };
    pyfhmdot = python-self.callPackage ./derivation.nix {
      fhmdot = python-self.fhmdot;
      src = ./.;
    };

  };

  python = python3.override (old: {
    packageOverrides = lib.composeExtensions (old.packageOverrides or (_: _: { }))
      pythonPackageOverrides;
  });

  pythonPackages = python.pkgs;

in
{ inherit pythonPackages; }


