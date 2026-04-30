interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	shared := 1
	other := 2
	process(shared.clone(), 1);
	process(other.clone(), 0);
	process(shared.clone(), 8);
}
