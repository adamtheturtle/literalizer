interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process(1, 2, 3, 4);
	process(5, 6, 7, 8);
}
