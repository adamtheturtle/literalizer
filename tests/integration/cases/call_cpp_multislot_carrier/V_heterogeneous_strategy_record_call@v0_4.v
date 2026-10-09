interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process(1, 'hello');
	process('two', false);
	process(3.5, unsafe { nil });
}
