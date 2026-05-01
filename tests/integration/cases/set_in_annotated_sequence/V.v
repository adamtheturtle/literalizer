interface IVal {}

fn main() {
	my_data := [
		IVal([]IVal{}),
		IVal([1, 2]),
		IVal([]IVal{}),
	]
	_ = my_data
}
