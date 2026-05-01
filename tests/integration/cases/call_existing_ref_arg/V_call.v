interface IVal {}
interface ICallArg_ {}
fn send(args ...ICallArg_) {}

fn main() {
	existing := 42
	send(existing);
}
