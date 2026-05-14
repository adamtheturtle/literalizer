interface IVal {}

fn main() {
	my_data := {
		'id': IVal(1),
		'description': IVal('example'),
		'is_done': IVal(false),
		'blocks': IVal([1, 2, 3]),
	}
	_ = my_data
}
