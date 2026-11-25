interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process("09:30:00");
	process("2024-01-15T00:00:00+00:00");
	process(1);
}
