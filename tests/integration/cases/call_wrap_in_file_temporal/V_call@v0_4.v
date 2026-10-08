interface ICallArg_ {}
fn check(args ...ICallArg_) {}

fn main() {
	check("2024-01-15T10:30:00+00:00", "2024-06-01");
}
