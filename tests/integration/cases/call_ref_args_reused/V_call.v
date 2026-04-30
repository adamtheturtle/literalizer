interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	repeated_var := 1
	single_var := [
		4,
		5,
		6,
	]
	process(repeated_var.clone(), 1);
	process(single_var.clone(), 0);
	process(repeated_var.clone(), 8);
}
