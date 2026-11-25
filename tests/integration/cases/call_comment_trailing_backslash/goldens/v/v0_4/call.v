interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process(1);  // trail \ .
	process(2);  // second
}
