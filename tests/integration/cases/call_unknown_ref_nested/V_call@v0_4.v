interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	known_value := true
	unknown_value := true
	process(known_value, [unknown_value]);
}
