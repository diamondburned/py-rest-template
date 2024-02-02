{
	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
		flake-utils.url = "github:numtide/flake-utils";
	};

	outputs =
		{ self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
			with nixpkgs.legacyPackages.${system};
			{
				devShell = mkShell {
					packages = [
						python3
						python3Packages.black
						python3Packages.greenlet
						pyright

						hurl
					];

					shellHook = ''
						python3 -m venv .venv
						source .venv/bin/activate
					'';
				};
			}
		);
}
