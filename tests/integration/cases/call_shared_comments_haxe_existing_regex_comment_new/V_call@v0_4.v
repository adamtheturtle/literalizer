interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := (~/\//).match("/") ? make_widget(42) : null // trailing
	_ = my_data
}
