interface IVal {}

fn main() {
	my_data := {
		'users': [{'name': IVal('Bob'), 'tags': IVal(['admin', 'user'])}, {'name': IVal('Carol'), 'tags': IVal(['guest'])}],
	}
	_ = my_data
}
