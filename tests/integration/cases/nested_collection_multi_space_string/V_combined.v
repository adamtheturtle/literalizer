interface IVal {}

fn main() {
	mut my_data := [
		{'key': IVal('hello   world'), 'value': IVal(1)},
	]
	my_data = [
		{'key': IVal('hello   world'), 'value': IVal(1)},
	]
	_ = my_data
}
