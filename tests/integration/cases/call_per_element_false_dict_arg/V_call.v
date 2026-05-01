interface IVal {}
interface ICallArg_ {}
fn send(args ...ICallArg_) {}

fn main() {
	send({'a': IVal(1), 'b': IVal('x')});
}
