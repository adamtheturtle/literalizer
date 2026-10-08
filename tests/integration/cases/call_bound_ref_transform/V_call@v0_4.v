interface ICallArg_ {}
fn f(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	ref_data := 1
	f(ref_data);
}
