interface ICallArg_ {}
fn put(args ...ICallArg_) {}
fn get(args ...ICallArg_) {}

fn main() {
	put(1, 10);
	get(1);
}
