interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_var := 42
	my_other := 7
	process([IVal({'ref': 'my_var'}), IVal(42), IVal('static')]);
	process([IVal({'ref': 'my_other'}), IVal(7), IVal('label')]);
}
