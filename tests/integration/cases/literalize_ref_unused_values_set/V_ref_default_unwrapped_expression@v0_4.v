interface ICallArg_ {}
fn consume_widget(args ...ICallArg_) {}

fn main() {
	consume_widget([
		1,
		2,
	]);
}
