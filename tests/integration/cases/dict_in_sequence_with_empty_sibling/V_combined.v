interface IVal {}

fn main() {
	mut my_data := [
		IVal({'a': 1}),
		IVal([]IVal{}),
	]
	my_data = [
		IVal({'a': 1}),
		IVal([]IVal{}),
	]
	_ = my_data
}
