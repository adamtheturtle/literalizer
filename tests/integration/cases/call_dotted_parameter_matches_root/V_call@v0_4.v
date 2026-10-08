interface ICallArg_ {}
struct OuterType_ {}
fn (r OuterType_) inner(args ...ICallArg_) {}

fn main() {
	outer := OuterType_{}
	outer.inner(1, 2);
}
