interface ICallArg_ {}
struct ObjType_ {}
fn (r ObjType_) ZKV(args ...ICallArg_) {}

fn main() {
	obj := ObjType_{}
	obj.ZKV(1);
}
