interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := unsafe { nil }
	consume(item);
}
