interface IVal {}
interface ICallArg_ {}
fn make_widget(args ...ICallArg_) {}

fn main() {
	make_widget([]IVal{});
}
