interface ICallArg_ {}
struct ClassType_ {}
fn (r ClassType_) member(args ...ICallArg_) {}

fn main() {
	class := ClassType_{}
	class.member(42);
}
