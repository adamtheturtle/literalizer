interface IVal {}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := [
		1,
		2,
	]
	consume(item);
}
