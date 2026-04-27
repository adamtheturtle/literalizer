interface IVal {}

fn main() {
	my_data := {
		'a': IVal({'x': 1}),
		'b': IVal(2),
	}
	_ = my_data
}
