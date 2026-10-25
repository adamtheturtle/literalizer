interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }
fn consume(args ...ICallArg_) {}

fn main() {
	mut my_data := make_widget(unsafe { nil })
	consume(my_data);
	my_data = make_widget(42) // note
	// extra
	consume(my_data);
}
