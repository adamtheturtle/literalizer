interface ICallArg_ {}
struct ClassType_ {}
fn (r ClassType_) member(arg0 ICallArg_) {}

fn main() {
	class := ClassType_{}
	class.member(42);
}
