interface ICallArg_ {}
fn record(args ...ICallArg_) ICallArg_ { return 0 }
fn flush(args ...ICallArg_) {}

fn main() {
	record(42);
	flush(3);
}
