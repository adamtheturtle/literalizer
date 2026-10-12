interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := (@"ends\" + "// payload").Length >= 0 ? make_widget(42) : make_widget(42)
	_ = my_data
}
