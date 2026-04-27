interface IVal {}

fn main() {
	my_data := {
		// comment
		'name': IVal('Alice'),
		'score': IVal(unsafe { nil }),
	}
	_ = my_data
}
