fn literalizer_ref_value[T](value T) T {
    $if T is $array_dynamic || T is $map {
        return value.clone()
    } $else {
        return value
    }
}
interface IVal {}
struct Record0 {
	name string
	values []int
}
interface ICallArg_ {}
fn consume(args ...ICallArg_) {}

fn main() {
	item := Record0{
		name: 'first',
		values: [
			1,
			2,
		],
	}
	consume(item);
}
