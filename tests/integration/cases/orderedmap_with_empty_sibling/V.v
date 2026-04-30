interface IVal {}

fn main() {
	my_data := [
		IVal({'a': 1}),
		IVal([]IVal{}),
	]
	_ = my_data
}
