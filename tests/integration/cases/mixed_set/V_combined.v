interface IVal {}

fn main() {
	mut my_data := [
		IVal(true),
		IVal(42),
		IVal('apple'),
	]
	my_data = [
		IVal(true),
		IVal(42),
		IVal('apple'),
	]
	_ = my_data
}
