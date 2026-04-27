interface IVal {}

fn main() {
	my_data := [
		IVal([]IVal{}),
		IVal(map[string]IVal{}),
	]
	_ = my_data
}
