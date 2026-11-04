interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	item := [
		1,
		2,
	]
	process(item);
	process(item);
}
