interface IVal {}

fn main() {
	mut my_data := {
		'outer': {'a': IVal(1), 'b': IVal('x'), 'c': IVal(unsafe { nil })},
	}
	my_data = {
		'outer': {'a': IVal(1), 'b': IVal('x'), 'c': IVal(unsafe { nil })},
	}
	_ = my_data
}
