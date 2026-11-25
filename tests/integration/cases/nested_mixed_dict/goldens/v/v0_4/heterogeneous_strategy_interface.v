interface IVal {}

fn main() {
	my_data := {
		'outer': {'a': IVal(1), 'b': IVal('x'), 'c': IVal(unsafe { nil })},
	}
	_ = my_data
}
