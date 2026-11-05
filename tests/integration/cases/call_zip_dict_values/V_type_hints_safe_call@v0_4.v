interface ICallArg_ {}
fn process(args ...ICallArg_) ICallArg_ { return 0 }
fn emit(args ...ICallArg_) {}

fn main() {
	emit(process('hello'), {'a': 1, 'b': 2});
	emit(process(42), {'c': 3, 'd': 4});
}
