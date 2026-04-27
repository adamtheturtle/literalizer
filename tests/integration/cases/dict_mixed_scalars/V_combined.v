interface IVal {}

fn main() {
	mut my_data := {
		'a': IVal(1),
		'b': IVal('x'),
	}
	my_data = {
		'a': IVal(1),
		'b': IVal('x'),
	}
	_ = my_data
}
