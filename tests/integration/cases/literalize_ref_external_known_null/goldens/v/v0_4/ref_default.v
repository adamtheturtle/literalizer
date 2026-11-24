fn literalizer_ref_value[T](value T) T {
    $if T is $array_dynamic || T is $map {
        return value.clone()
    } $else {
        return value
    }
}
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
