interface IVal {}

fn main() {
	my_data := [
		{'id': IVal(1), 'label': IVal('first')},
		{'id': IVal(2), 'label': IVal('second')},
		{'id': IVal(3), 'label': IVal('third')},
	]
	_ = my_data
}
