interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }
fn consume_widget(args ...ICallArg_) {}

fn main() {
	mut my_data := make_widget(42)
	consume_widget(my_data);
	my_data = make_widget(my_data)
	// note
	consume_widget(my_data);
}
