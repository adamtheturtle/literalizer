interface IVal {}

fn main() {
	my_data := {
		'id': IVal(1),
		'label': IVal('She said "hello", then waved'),
		'enabled': IVal(false),
		'related_ids': IVal([1, 2, 3]),
	}
	_ = my_data
}
