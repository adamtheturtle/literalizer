interface IVal {}

fn main() {
	mut my_data := {
		'a': IVal(map[string]IVal{}),
		'b': IVal(1),
	}
	my_data = {
		'a': IVal(map[string]IVal{}),
		'b': IVal(1),
	}
	_ = my_data
}
