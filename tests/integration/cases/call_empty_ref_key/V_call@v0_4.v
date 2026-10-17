interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	external_value := 1
	consume(external_value);
}
