interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_var := 42
	process({'key': my_var, 'count': 42});
}
