interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	mut my_data := make_widget(unsafe { nil })
	my_data = make_widget(42) // note
	// extra
}
