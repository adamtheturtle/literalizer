interface IVal {}

fn main() {
	my_data := [
		IVal(map[string]IVal{}),
		IVal([]IVal{}),
	]
	_ = my_data
}
