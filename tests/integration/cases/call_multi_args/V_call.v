interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process(1, 42);
	process(2, 100);
}
