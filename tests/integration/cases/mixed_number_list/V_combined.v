interface IVal {}

fn main() {
	mut my_data := [
		IVal(1),
		IVal(2.5),
		IVal(3),
	]
	my_data = [
		IVal(1),
		IVal(2.5),
		IVal(3),
	]
	_ = my_data
}
