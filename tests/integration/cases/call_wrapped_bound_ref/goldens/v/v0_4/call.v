interface ICallArg_ {}
fn make_widget(args ...ICallArg_) {}

fn main() {
	value := 1
	make_widget(value);
}
