interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := 42
	consume({'field': item});
}
