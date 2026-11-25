interface ICallArg_ {}
fn f(args ...ICallArg_) ICallArg_ { return 0 }
fn repr(args ...ICallArg_) {}

fn main() {
	ref_data := 1
	repr(f(ref_data));
}
