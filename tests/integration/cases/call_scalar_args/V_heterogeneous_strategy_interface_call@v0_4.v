interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process('hello');
	process(42);
	process(true);
}
