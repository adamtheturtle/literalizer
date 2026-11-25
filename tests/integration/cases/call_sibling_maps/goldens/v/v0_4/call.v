interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process({'value': 1});
	process({'value': 'hello'});
}
