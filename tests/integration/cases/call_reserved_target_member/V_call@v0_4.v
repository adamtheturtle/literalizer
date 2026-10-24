interface ICallArg_ {}
struct ObjType_ {}
fn (r ObjType_) class(arg0 ICallArg_) {}

fn main() {
	obj := ObjType_{}
	obj.class(42);
}
