interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_var := 42
	process({'key': IVal(my_var), 'count': IVal(42)});
}
