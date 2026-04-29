interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_var := 42
	my_other := 7
	process([IVal(my_var.clone()), IVal(42), IVal('static')]);
	process([IVal(my_other.clone()), IVal(7), IVal('label')]);
}
