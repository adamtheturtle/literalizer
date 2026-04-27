interface IVal {}

fn main() {
	mut my_data := [
		{'name': IVal('Alice'), 'age': IVal(30)},
		{'name': IVal('Bob'), 'age': IVal(25)},
	]
	my_data = [
		{'name': IVal('Alice'), 'age': IVal(30)},
		{'name': IVal('Bob'), 'age': IVal(25)},
	]
	_ = my_data
}
