interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process(1);  // note<U+2028>still commented<U+2029>done
}
