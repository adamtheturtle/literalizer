interface ICallArg_ {}
struct ObjType_ {}
fn (r ObjType_) ZVal(args ...ICallArg_) {}

fn main() {
	obj := ObjType_{}
	obj.ZVal(1);
}
