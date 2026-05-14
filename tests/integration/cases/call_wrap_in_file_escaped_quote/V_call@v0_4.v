interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process('a"b');
}
