interface IVal {}

fn main() {
	my_data := {
		'call': IVal('send'),
		'args': IVal([IVal(1), IVal('email'), IVal('a@gmail.com'), IVal(100)]),
	}
	_ = my_data
}
