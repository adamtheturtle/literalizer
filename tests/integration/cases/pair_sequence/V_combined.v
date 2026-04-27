interface IVal {}

fn main() {
	mut my_data := [
		IVal(1),
		IVal('hello'),
	]
	my_data = [
		IVal(1),
		IVal('hello'),
	]
	_ = my_data
}
