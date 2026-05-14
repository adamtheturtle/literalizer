interface IVal {}

fn main() {
	my_data := {
		'name': IVal('Alice'),
		'age': IVal(30),
		'active': IVal(true),
	}
	_ = my_data
}
