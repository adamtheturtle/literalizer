interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_var := 42
	process([IVal({'ref': 'myVar'}), IVal(42), IVal('static')]);
}
