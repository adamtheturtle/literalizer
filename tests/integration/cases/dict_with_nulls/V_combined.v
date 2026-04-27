interface IVal {}

fn main() {
	mut my_data := {
		'name': IVal('Alice'),
		'score': IVal(unsafe { nil }),
		'age': IVal(30),
	}
	my_data = {
		'name': IVal('Alice'),
		'score': IVal(unsafe { nil }),
		'age': IVal(30),
	}
	_ = my_data
}
