interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }
fn consume_widget(args ...ICallArg_) {}

fn main() {
	mut my_data := make_widget(0)
	consume_widget(my_data);
	my_data = make_widget(1)
	consume_widget(my_data);
}
