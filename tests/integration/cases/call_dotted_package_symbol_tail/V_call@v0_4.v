interface ICallArg_ {}
struct HelperType_ {}
fn (r HelperType_) list(args ...ICallArg_) {}

fn main() {
	helper := HelperType_{}
	helper.list(1);
}
