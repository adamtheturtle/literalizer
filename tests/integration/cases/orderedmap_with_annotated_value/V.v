interface IVal {}

fn main() {
	my_data := {
		'a': IVal([]IVal{}),
		'b': IVal(1),
	}
	_ = my_data
}
