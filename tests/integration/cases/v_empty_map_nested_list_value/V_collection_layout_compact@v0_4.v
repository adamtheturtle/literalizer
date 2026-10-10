interface IVal {}

fn main() {
	my_data := [
		[{'values': [[]IVal{}]}, map[string][][]IVal{}],
		[map[string][][]IVal{}, {'values': [[]IVal{}]}],
	]
	_ = my_data
}
