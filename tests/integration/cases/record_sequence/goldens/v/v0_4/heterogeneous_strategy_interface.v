interface IVal {}

fn main() {
	my_data := [
		{'id': IVal(1), 'label': IVal('first'), 'tags': IVal([]IVal{})},
		{'id': IVal(2), 'label': IVal('second'), 'tags': IVal([]IVal{})},
		{'id': IVal(3), 'label': IVal('third'), 'tags': IVal([]IVal{})},
	]
	_ = my_data
}
