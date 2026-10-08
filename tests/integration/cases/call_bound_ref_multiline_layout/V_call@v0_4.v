interface ICallArg_ {}
fn f(args ...ICallArg_) {}

fn main() {
	x := [
		[
			1,
			2,
		],
		[
			3,
			4,
		],
	]
	f([
		[
			x,
		],
	]);
}
