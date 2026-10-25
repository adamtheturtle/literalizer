interface IVal {}
interface ICallArg_ {}
fn consume_widget(args ...ICallArg_) {}

fn main() {
	ref_data := [
		1,
		2,
	]
	mut my_data := [
		0,
	]
	consume_widget(my_data);
	my_data = ref_data.clone()
	consume_widget(my_data);
}
