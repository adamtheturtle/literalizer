interface IVal {}

fn main() {
	my_data := [
		{'call': IVal('send'), 'args': IVal([IVal(1), IVal('email'), IVal('a@gmail.com'), IVal(100)])},
		{'call': IVal('recv'), 'args': IVal([IVal(2), IVal('sms'), IVal('b@example.com'), IVal(200)])},
	]
	_ = my_data
}
