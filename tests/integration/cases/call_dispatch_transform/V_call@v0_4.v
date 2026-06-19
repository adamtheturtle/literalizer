interface ICallArg_ {}
fn record_value(args ...ICallArg_) ICallArg_ { return 0 }
fn flush_buffer(args ...ICallArg_) {}
fn emit(args ...ICallArg_) {}

fn main() {
	emit(record_value(42));
	flush_buffer(3);
}
