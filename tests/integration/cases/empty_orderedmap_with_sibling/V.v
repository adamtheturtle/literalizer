interface IVal {}

fn main() {
	my_data := [
		IVal({}),
		IVal([]IVal{}),
	]
	_ = my_data
}
