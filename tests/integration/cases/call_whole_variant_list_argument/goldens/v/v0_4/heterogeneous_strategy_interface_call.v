interface IVal {}
interface ICallArg_ {}
fn f(args ...ICallArg_) {}

fn main() {
	f([IVal(1), IVal('x')]);
}
