interface IVal {}

fn main() {
	mut my_data := [
		IVal(1),
		IVal('hello'),
		IVal(true),
	]
	my_data = [
		IVal(1),
		IVal('hello'),
		IVal(true),
	]
	_ = my_data
}
