interface IVal {}
interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := make_widget([]IVal{})
	_ = my_data
}
