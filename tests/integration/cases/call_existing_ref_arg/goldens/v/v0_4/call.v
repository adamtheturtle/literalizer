interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	existing := 42
	process(existing);
}
