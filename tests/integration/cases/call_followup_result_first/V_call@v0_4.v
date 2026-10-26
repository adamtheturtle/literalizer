fn literalizer_ref_value[T](value T) T {
    $if T is $array_dynamic || T is $map {
        return value.clone()
    } $else {
        return value
    }
}
interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }
fn consume(args ...ICallArg_) {}

fn main() {
	my_data := make_widget(42, 3)
	consume(my_data, 3);
}
