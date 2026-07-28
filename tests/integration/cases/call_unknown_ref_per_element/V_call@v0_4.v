interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	unknown_value := []IVal{}
	process(unknown_value);
}
