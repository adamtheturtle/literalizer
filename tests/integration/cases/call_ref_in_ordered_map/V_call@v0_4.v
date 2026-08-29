interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	big_list := [
		'x',
	]
	process({'m': big_list});
}
