interface ICallArg_ {}
fn f(args ...ICallArg_) {}

fn main() {
	// calls heading
	// before call one
	// first argument
	f(1, 2);  // after call one
	// second argument
	f(3, 4);
	// after all calls
}
