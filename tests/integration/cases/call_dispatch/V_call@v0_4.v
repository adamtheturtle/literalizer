interface ICallArg_ {}
fn store_item(args ...ICallArg_) {}
fn read_item(args ...ICallArg_) {}

fn main() {
	store_item(1, 10);
	read_item(1);
}
