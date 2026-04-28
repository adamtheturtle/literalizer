interface IVal {}

fn main() {
	mut my_data := {
		// comment
		'name': IVal('Alice'),
		'score': IVal(unsafe { nil }),
	}
	my_data = {
		// comment
		'name': IVal('Alice'),
		'score': IVal(unsafe { nil }),
	}
	_ = my_data
}
