interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := ("${ /* } " block */ 42 // } " line
	}").length >= 0 ? make_widget(42) : make_widget(42) // trailing
	// extra
	_ = my_data
}
