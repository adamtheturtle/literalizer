interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process({'value': IVal(1)});
	process({'value': IVal('hello')});
}
