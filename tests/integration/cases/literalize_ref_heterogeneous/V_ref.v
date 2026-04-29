interface IVal {}

fn main() {
	my_data := {
		'a': IVal(1),
		'b': IVal('hello'),
	}
	_ = my_data
}
