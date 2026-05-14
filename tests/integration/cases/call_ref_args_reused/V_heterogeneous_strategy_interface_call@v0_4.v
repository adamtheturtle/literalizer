interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	single_var := [
		4,
		5,
		6,
	]
	repeated_var := 1
	process(repeated_var, 1);
	process(single_var, 0);
	process(repeated_var, 8);
}
