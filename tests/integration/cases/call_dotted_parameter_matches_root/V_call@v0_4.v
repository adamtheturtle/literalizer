interface ICallArg_ {}
struct OuterType_ {}
fn (r OuterType_) inner(arg0 ICallArg_, arg1 ICallArg_) {}

fn main() {
	outer := OuterType_{}
	outer.inner(1, 2);
}
