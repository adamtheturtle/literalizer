fn literalizer_ref_value[T](value T) T {
    $if T is $array_dynamic || T is $map {
        return value.clone()
    } $else {
        return value
    }
}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	known_value := true
	unknown_value := true
	process(known_value, unknown_value);
}
