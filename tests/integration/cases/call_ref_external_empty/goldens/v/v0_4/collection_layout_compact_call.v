interface IVal {}
fn literalizer_ref_value[T](value T) T {
    $if T is $array_dynamic || T is $map {
        return value.clone()
    } $else {
        return value
    }
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := [
		1,
		2,
	]
	consume(item);
}
