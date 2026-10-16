interface IVal {}
interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	items := []IVal{}
	make_widget(items);
}
