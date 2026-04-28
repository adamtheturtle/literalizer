interface IVal {}

fn main() {
	my_data := [
		IVal(42),
		IVal(3.14),
		IVal(true),
		IVal(false),
		IVal('hello "world"'),
	]
	_ = my_data
}
