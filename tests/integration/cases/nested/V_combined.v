interface IVal {}

fn main() {
	mut my_data := {
		'users': [{'name': IVal('Bob'), 'tags': IVal(['admin', 'user'])}, {'name': IVal('Carol'), 'tags': IVal(['guest'])}],
	}
	my_data = {
		'users': [{'name': IVal('Bob'), 'tags': IVal(['admin', 'user'])}, {'name': IVal('Carol'), 'tags': IVal(['guest'])}],
	}
	_ = my_data
}
