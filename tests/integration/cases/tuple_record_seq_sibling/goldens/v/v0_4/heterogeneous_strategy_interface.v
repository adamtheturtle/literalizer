interface IVal {}

fn main() {
	my_data := {
		'scores': [IVal(10), IVal(20), IVal(30)],
		'args': [IVal(1), IVal('email'), IVal('a@gmail.com'), IVal(100)],
	}
	_ = my_data
}
