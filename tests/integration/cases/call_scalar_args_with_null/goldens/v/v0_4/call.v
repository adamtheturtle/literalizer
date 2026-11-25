interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process(unsafe { nil });
	process('hello');
}
