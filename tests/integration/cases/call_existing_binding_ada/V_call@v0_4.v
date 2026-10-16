interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	mut my_data := make_widget(0)
	make_widget(my_data);
	my_data = make_widget(1)
	make_widget(my_data);
}
