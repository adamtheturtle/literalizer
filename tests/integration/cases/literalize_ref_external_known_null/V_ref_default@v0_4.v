interface IVal {}
interface ICallArg_ {}
fn consume_widget(args ...ICallArg_) {}

fn main() {
	item := unsafe { nil }
	mut my_data := unsafe { nil }
	consume_widget(my_data);
	my_data = item
	consume_widget(my_data);
}
