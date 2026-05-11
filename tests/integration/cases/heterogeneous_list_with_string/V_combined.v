interface IVal {}

fn main() {
	mut my_data := [
		IVal('hello'),
		IVal(42),
	]
	my_data = [
		IVal('hello'),
		IVal(42),
	]
	_ = my_data
}
