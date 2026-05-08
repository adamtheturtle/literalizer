interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_ints := [
		1,
		2,
		3,
	]
	my_strings := [
		'a',
		'b',
	]
	process(my_ints, 42);
	process(my_strings, 7);
}
