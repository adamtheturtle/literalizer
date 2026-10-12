interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := 42
	my_data = make_widget(my_data) // note
	make_widget(my_data);
}
