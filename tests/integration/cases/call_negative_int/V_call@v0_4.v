interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process(-1);
	process(-2);
	process(-3);
}
