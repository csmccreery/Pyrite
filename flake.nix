{
	description = "Pyrite is a portable and composable tool for building static websites from a variety of markup languages";
	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
	};

	outputs = { self, nixpkgs, ... }@inputs:
	let
		system = "x86_64-linux";
		pkgs = import nixpkgs { inherit system; };
	in {
		devShells.${system}.default = pkgs.mkShell {
			buildInputs = [
				pkgs.python315
                pkgs.pyright
                pkgs.black
				pkgs.bootdev-cli
				pkgs.docker
				pkgs.uv
			];
		};
	};
}
