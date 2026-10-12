interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := (`__LINE__ > 0) ? make_widget(42) : make_widget(42) // trailing `marker
	_ = my_data
}
