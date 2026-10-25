interface ICallArg_ {}
fn process(args ...ICallArg_) ICallArg_ { return 0 }
interface ICallArg_ {}
struct HelpersType_ {}
fn (r HelpersType_) emit(arg0 ICallArg_, arg1 ICallArg_) {}

fn main() {
	helpers := HelpersType_{}
	helpers.emit(process(1), 42);
}
