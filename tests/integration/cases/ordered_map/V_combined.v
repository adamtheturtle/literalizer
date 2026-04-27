interface IVal {}

fn main() {
	mut my_data := {
		'name': IVal('Alice'),
		'age': IVal(30),
		'active': IVal(true),
	}
	my_data = {
		'name': IVal('Alice'),
		'age': IVal(30),
		'active': IVal(true),
	}
	_ = my_data
}
