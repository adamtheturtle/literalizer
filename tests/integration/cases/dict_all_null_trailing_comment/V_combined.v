interface IVal {}

fn main() {
	mut my_data := {
		'a': IVal(unsafe { nil }),
		'b': IVal(unsafe { nil }),
		// trailing
	}
	my_data = {
		'a': IVal(unsafe { nil }),
		'b': IVal(unsafe { nil }),
		// trailing
	}
	_ = my_data
}
