interface ICallArg_ {}
fn process(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	process('time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)');
}
