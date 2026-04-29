interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_var := 42
	process([IVal(my_var.clone()), IVal(42), IVal('static')]);
}
