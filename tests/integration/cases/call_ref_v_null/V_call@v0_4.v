interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	value := unsafe { nil }
	consume(value);
}
