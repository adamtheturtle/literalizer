interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_var := [
		1,
		2,
		3,
	]
	process(my_var.clone());
}
