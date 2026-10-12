interface ICallArg_ {}
struct ObjType_ {}
fn (r ObjType_) class(args ...ICallArg_) {}

fn main() {
	obj := ObjType_{}
	obj.class(42);
}
