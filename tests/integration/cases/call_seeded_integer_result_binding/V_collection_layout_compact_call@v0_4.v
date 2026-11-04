interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }
fn consume(args ...ICallArg_) {}

fn main() {
	mut my_data := make_widget(42)
	consume(my_data);
	my_data = make_widget(42)
	consume(my_data);
}
