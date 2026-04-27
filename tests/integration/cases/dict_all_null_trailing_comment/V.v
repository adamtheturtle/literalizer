interface IVal {}

fn main() {
	my_data := {
		'a': IVal(unsafe { nil }),
		'b': IVal(unsafe { nil }),
		// trailing
	}
	_ = my_data
}
