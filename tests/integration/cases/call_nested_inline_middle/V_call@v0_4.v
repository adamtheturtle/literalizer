interface ICallArg_ {}
fn f(args ...ICallArg_) {}

fn main() {
	f([['DEL', 'b', '10'], ['ADD', 'a', 'x']]);  // note
	// next call
	f([['ADD', 'c', 'y']]);
}
