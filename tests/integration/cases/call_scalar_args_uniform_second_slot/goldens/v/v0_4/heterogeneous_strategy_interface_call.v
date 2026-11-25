interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process('hello', 'a');
	process(42, 'b');
	process(true, 'c');
}
