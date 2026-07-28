interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	unknown_value := [
		1,
	]
	process(unknown_value);
}
