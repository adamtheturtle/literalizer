interface IVal {}

fn main() {
	mut my_data := [
		IVal("48656c6c6f"),
		IVal([]IVal{}),
	]
	my_data = [
		IVal("48656c6c6f"),
		IVal([]IVal{}),
	]
	_ = my_data
}
