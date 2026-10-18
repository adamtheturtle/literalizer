interface ICallArg_ {}
fn f(args ...ICallArg_) {}

fn main() {
	ref_data := [
		1,
		2,
	]
	f([
		ref_data,
	]);
	f([
		ref_data,
	]);
}
