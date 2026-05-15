interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data = make_widget(42)
	_ = my_data
}
