interface IVal {}

fn main() {
	my_data := {
		'a': IVal(1),
		'b': IVal(2.5),
		'c': IVal(3),
	}
	_ = my_data
}
