interface IVal {}

fn main() {
	my_data := {
		'a': IVal(1),
		'b': IVal('x'),
	}
	_ = my_data
}
