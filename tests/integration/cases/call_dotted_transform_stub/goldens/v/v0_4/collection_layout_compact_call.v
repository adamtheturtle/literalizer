interface ICallArg_ {}
fn process(args ...ICallArg_) ICallArg_ { return 0 }
struct TracerType_ {}
fn (r TracerType_) emit(arg0 ICallArg_) {}

fn main() {
	tracer := TracerType_{}
	tracer.emit(process('hello'));
	tracer.emit(process(42));
	tracer.emit(process(true));
}
