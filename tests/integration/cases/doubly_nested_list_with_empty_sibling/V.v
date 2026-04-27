interface IVal {}

fn main() {
	my_data := [
		IVal([[1, 2]]),
		IVal([]IVal{}),
		IVal([[3, 4]]),
	]
	_ = my_data
}
