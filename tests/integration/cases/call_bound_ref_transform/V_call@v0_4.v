interface ICallArg_ {}
fn f(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	x := 1
	f(x);
}
