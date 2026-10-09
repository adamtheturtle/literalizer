interface IVal {}

fn main() {
	my_data := [
		{'count': IVal(1), 'name': IVal('value')},
		map[string]IVal{},
	]
	_ = my_data
}
