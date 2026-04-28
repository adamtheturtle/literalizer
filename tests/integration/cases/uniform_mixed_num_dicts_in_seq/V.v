interface IVal {}

fn main() {
	my_data := [
		{'x': IVal(1), 'y': IVal(2.5)},
		{'x': IVal(3), 'y': IVal(4.0)},
	]
	_ = my_data
}
