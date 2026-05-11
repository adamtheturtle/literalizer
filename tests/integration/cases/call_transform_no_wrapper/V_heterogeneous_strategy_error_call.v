interface ICallArg_ {}
fn process(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	process('hello');
	process(42);
	process(true);
}
