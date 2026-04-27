interface IVal {}

fn main() {
	my_data := [
		{'name': IVal('Alice'), 'age': IVal(30)},
		{'name': IVal('Bob'), 'age': IVal(25)},
	]
	_ = my_data
}
