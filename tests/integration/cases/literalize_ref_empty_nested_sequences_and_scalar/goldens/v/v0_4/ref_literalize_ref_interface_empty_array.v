interface IVal {}

fn main() {
	seed := 1
	my_data := [
		IVal([]IVal{}),
		IVal([[]IVal{}]),
		IVal(seed),
	]
	_ = my_data
}
