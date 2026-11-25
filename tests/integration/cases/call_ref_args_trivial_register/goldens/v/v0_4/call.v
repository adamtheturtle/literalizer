interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_int := 1
	my_bool := true
	my_float := 3.14
	my_list := [
		1,
		2,
		3,
	]
	process(my_int, 42);
	process(my_bool, 7);
	process(my_float, 9);
	process(my_list, 1);
}
