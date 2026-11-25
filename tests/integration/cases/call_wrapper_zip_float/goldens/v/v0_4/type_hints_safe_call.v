interface ICallArg_ {}
fn process(args ...ICallArg_) ICallArg_ { return 0 }
fn emit(args ...ICallArg_) {}

fn main() {
	emit(process(1), 1.5);
}
