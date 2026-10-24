interface ICallArg_ {}
fn check_wrapper(args ...ICallArg_) {}

fn main() {
	check_wrapper(42);
}
