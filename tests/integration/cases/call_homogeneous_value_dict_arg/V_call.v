interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	process({'a': 1, 'b': 2});
}
