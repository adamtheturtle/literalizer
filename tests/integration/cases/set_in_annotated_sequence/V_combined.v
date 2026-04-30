interface IVal {}

fn main() {
	mut my_data := [
		IVal([]IVal{}),
		IVal([1, 2]),
		IVal([]IVal{}),
	]
	my_data = [
		IVal([]IVal{}),
		IVal([1, 2]),
		IVal([]IVal{}),
	]
	_ = my_data
}
