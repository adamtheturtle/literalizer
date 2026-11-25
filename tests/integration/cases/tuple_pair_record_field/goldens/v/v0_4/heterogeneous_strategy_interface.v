interface IVal {}

fn main() {
	my_data := {
		'call': IVal('send'),
		'args': IVal([IVal(1), IVal('email')]),
	}
	_ = my_data
}
