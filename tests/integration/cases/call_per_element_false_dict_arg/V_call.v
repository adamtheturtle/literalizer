interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process({'a': IVal(1), 'b': IVal('x')});
}
