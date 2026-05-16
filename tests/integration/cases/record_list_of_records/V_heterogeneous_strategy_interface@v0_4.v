interface IVal {}

fn main() {
	my_data := {
		'name': IVal('box'),
		'items': IVal([{'id': IVal(1), 'label': IVal('first')}, {'id': IVal(2), 'label': IVal('second')}]),
	}
	_ = my_data
}
