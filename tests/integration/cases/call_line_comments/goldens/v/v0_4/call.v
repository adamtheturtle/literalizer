interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process('Dune');  // first edition
	process('Solaris');
	process('Neuromancer');  // cyberpunk
}
