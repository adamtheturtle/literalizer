interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := 's'
	consume(item);
}
