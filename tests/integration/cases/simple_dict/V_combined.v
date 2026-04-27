interface IVal {}

fn main() {
	mut my_data := {
		'name': IVal('Alice'),
		'age': IVal(30),
		'active': IVal(true),
		'score': IVal(unsafe { nil }),
	}
	my_data = {
		'name': IVal('Alice'),
		'age': IVal(30),
		'active': IVal(true),
		'score': IVal(unsafe { nil }),
	}
	_ = my_data
}
