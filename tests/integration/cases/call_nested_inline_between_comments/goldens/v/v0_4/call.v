interface ICallArg_ {}
fn f(args ...ICallArg_) {}

fn main() {
	f(2, 'hello');  // trailing note
	// next element
	f(3, 'world');
}
