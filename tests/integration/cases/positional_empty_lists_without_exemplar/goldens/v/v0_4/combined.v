interface IVal {}

fn main() {
	mut my_data := [
		[][]IVal([[]IVal{}]),
		[][]IVal([[]IVal{}]),
	]
	my_data = [
		[][]IVal([[]IVal{}]),
		[][]IVal([[]IVal{}]),
	]
	_ = my_data
}
