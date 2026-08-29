interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	big_list := [
		'x',
	]
	process({'k': big_list}, 2);
}
