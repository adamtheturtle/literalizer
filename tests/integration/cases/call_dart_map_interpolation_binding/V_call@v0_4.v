interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := "${{'value': '// payload'}['value']}" // trailing
	// extra
	_ = my_data
}
