interface IVal {}

fn main() {
	my_data := {
		'name': IVal('Alice'),
		'age': IVal(30),
		'active': IVal(true),
		'score': IVal(4.5),
	}
	_ = my_data
}
