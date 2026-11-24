interface IVal {}
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
	my_list := {
		'unused': 'value',
	}
	process([[{'inner': my_list}]]);
}
