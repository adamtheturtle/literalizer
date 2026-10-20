interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	my_null := unsafe { nil }
	regular_null := unsafe { nil }
	consume(my_null);
	consume(regular_null);
}
