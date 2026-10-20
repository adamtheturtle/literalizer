interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	value := 1
	process(value);
}
